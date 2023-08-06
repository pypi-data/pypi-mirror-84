from __future__ import annotations

import datetime
from typing import Optional, Type
import traceback

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from .context import LogContext
from .model_mixin import SaveLogMixin


class LogMiddleware(BaseHTTPMiddleware):
    request_patched: bool = False

    save_model_class: Optional[Type[SaveLogMixin]]

    def patch_request_body(self):
        if self.request_patched:
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
        self.request_patched = True

    def __init__(self, save_model_class: Optional[Type[SaveLogMixin]], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save_model_class = save_model_class
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
            if self.save_model_class:
                await self.save_model_class.save_log(log_context, request=request, response=response)
