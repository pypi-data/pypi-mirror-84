import asyncio
import functools
import warnings
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Iterable,
    Mapping,
    Optional,
    Type,
    Union,
    cast,
    overload,
)

import jinja2
from aiohttp import web
from aiohttp.abc import AbstractView

from .helpers import GLOBAL_HELPERS
from .typedefs import Filters

__version__ = "1.3.0a0"

__all__ = ("setup", "get_env", "render_template", "render_string", "template")


APP_CONTEXT_PROCESSORS_KEY = "aiohttp_jinja2_context_processors"
APP_KEY = "aiohttp_jinja2_environment"
REQUEST_CONTEXT_KEY = "aiohttp_jinja2_context"

_SimpleHandler = Callable[[web.Request], Awaitable[web.StreamResponse]]
_MethodHandler = Callable[[Any, web.Request], Awaitable[web.StreamResponse]]
_ViewHandler = Callable[[Type[AbstractView]], Awaitable[web.StreamResponse]]
_HandlerType = Union[_SimpleHandler, _MethodHandler, _ViewHandler]
_TemplateReturnType = Awaitable[Union[web.StreamResponse, Mapping[str, Any]]]
_SimpleTemplateHandler = Callable[[web.Request], _TemplateReturnType]
_MethodTemplateHandler = Callable[[Any, web.Request], _TemplateReturnType]
_ViewTemplateHandler = Callable[[AbstractView], _TemplateReturnType]
_TemplateHandler = Union[
    _SimpleTemplateHandler, _MethodTemplateHandler, _ViewTemplateHandler
]


def setup(
    app: web.Application,
    *args: Any,
    app_key: str = APP_KEY,
    context_processors: Iterable[Callable[[web.Request], Dict[str, Any]]] = (),
    filters: Optional[Filters] = None,
    default_helpers: bool = True,
    **kwargs: Any,
) -> jinja2.Environment:
    kwargs.setdefault("autoescape", True)
    env = jinja2.Environment(*args, **kwargs)
    if default_helpers:
        env.globals.update(GLOBAL_HELPERS)
    if filters is not None:
        env.filters.update(filters)
    app[app_key] = env
    if context_processors:
        app[APP_CONTEXT_PROCESSORS_KEY] = context_processors
        app.middlewares.append(context_processors_middleware)

    env.globals["app"] = app

    return env


def get_env(app: web.Application, *, app_key: str = APP_KEY) -> jinja2.Environment:
    return cast(jinja2.Environment, app.get(app_key))


def render_string(
    template_name: str,
    request: web.Request,
    context: Mapping[str, Any],
    *,
    app_key: str = APP_KEY,
) -> str:
    env = request.config_dict.get(app_key)
    if env is None:
        text = (
            "Template engine is not initialized, "
            "call aiohttp_jinja2.setup(..., app_key={}) first"
            "".format(app_key)
        )
        # in order to see meaningful exception message both: on console
        # output and rendered page we add same message to *reason* and
        # *text* arguments.
        raise web.HTTPInternalServerError(reason=text, text=text)
    try:
        template = env.get_template(template_name)
    except jinja2.TemplateNotFound as e:
        text = f"Template '{template_name}' not found"
        raise web.HTTPInternalServerError(reason=text, text=text) from e
    if not isinstance(context, Mapping):
        text = "context should be mapping, not {}".format(type(context))
        # same reason as above
        raise web.HTTPInternalServerError(reason=text, text=text)
    if request.get(REQUEST_CONTEXT_KEY):
        context = dict(request[REQUEST_CONTEXT_KEY], **context)
    text = template.render(context)
    return text


def render_template(
    template_name: str,
    request: web.Request,
    context: Mapping[str, Any],
    *,
    app_key: str = APP_KEY,
    encoding: str = "utf-8",
    status: int = 200,
) -> web.Response:
    response = web.Response(status=status)
    if context is None:
        context = {}
    text = render_string(template_name, request, context, app_key=app_key)
    response.content_type = "text/html"
    response.charset = encoding
    response.text = text
    return response


def template(
    template_name: str,
    *,
    app_key: str = APP_KEY,
    encoding: str = "utf-8",
    status: int = 200,
) -> Callable[[_TemplateHandler], _HandlerType]:
    def wrapper(func: _TemplateHandler) -> _HandlerType:
        @overload
        async def wrapped(request: web.Request) -> web.StreamResponse:
            ...

        @overload
        async def wrapped(view: AbstractView) -> web.StreamResponse:
            ...

        @overload
        async def wrapped(_self: Any, request: web.Request) -> web.StreamResponse:
            ...

        @functools.wraps(func)
        async def wrapped(*args: Any) -> web.StreamResponse:
            if asyncio.iscoroutinefunction(func):
                coro = func
            else:
                warnings.warn(
                    "Bare functions are deprecated, " "use async ones",
                    DeprecationWarning,
                )
                coro = asyncio.coroutine(func)
            context = await coro(*args)
            if isinstance(context, web.StreamResponse):
                return context

            # Supports class based views see web.View
            if isinstance(args[0], AbstractView):
                request = args[0].request
            else:
                request = args[-1]

            response = render_template(
                template_name, request, context, app_key=app_key, encoding=encoding
            )
            response.set_status(status)
            return response

        return wrapped

    return wrapper


@web.middleware
async def context_processors_middleware(
    request: web.Request,
    handler: Callable[[web.Request], Awaitable[web.StreamResponse]],
) -> web.StreamResponse:

    if REQUEST_CONTEXT_KEY not in request:
        request[REQUEST_CONTEXT_KEY] = {}
    for processor in request.config_dict[APP_CONTEXT_PROCESSORS_KEY]:
        request[REQUEST_CONTEXT_KEY].update(await processor(request))
    return await handler(request)


async def request_processor(request: web.Request) -> Dict[str, web.Request]:
    return {"request": request}
