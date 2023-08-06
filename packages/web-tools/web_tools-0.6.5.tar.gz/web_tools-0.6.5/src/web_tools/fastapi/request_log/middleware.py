from __future__ import annotations

import datetime
from typing import Optional, Callable, Awaitable
import traceback

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from .context import LogContext

ContextHandler = Callable[[LogContext, Optional[Request], Optional[Response]], Awaitable[None]]


class LogMiddleware(BaseHTTPMiddleware):
    request_patched: bool = False

    context_handler: Optional[ContextHandler]

    @classmethod
    def patch_request_body(cls):
        if cls.request_patched:
            return

        body_original = Request.body

        async def body_patched(request: Request):
            body_content_key = 'body_content'
            body_content = request.scope.get(body_content_key)
            if body_content:
                return body_content
            body_content = await body_original(request)
            request.scope[body_content_key] = body_content
            return body_content

        Request.body = body_patched
        cls.request_patched = True

    def __init__(self, context_handler: Optional[ContextHandler] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context_handler = context_handler
        self.patch_request_body()

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_datetime = datetime.datetime.utcnow()
        exception_traceback = None
        response = None
        try:
            response = await call_next(request)
            return response
        except Exception:
            exception_traceback = traceback.format_exc()
            raise
        finally:
            response_datetime = datetime.datetime.utcnow()
            log_context = await LogContext.create(request_datetime, request, response_datetime,
                                                  response=response, exception_traceback=exception_traceback)
            if self.context_handler:
                await self.context_handler(log_context, request, response)
