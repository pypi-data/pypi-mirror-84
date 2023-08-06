import datetime
import traceback
from typing import Callable, Awaitable, Optional

from aiohttp import TraceConfig

from .context import LogContext

ContextHandler = Callable[[LogContext], Awaitable[None]]


class RequestLogTraceConfig(TraceConfig):
    context_handler: Optional[ContextHandler]

    def __init__(self, context_handler: Optional[ContextHandler] = None):
        self.context_handler = context_handler
        # noinspection PyTypeChecker
        super().__init__(trace_config_ctx_factory=LogContext.create_context)
        self.on_request_start.append(self.request_start)
        self.on_request_chunk_sent.append(self.request_chunk_sent)
        self.on_request_end.append(self.request_end)
        self.on_request_exception.append(self.request_exception)

    async def call_context_handler(self, trace_config_ctx: LogContext):
        if self.context_handler is None:
            return
        await self.context_handler(trace_config_ctx)

    async def request_start(self, session, trace_config_ctx: LogContext, params):
        trace_config_ctx.request_datetime = datetime.datetime.utcnow()
        trace_config_ctx.request_url = str(params.url)
        trace_config_ctx.request_method = params.method
        trace_config_ctx.request_headers = {}
        for k, v in params.headers.items():
            trace_config_ctx.request_headers[k] = v

    async def request_chunk_sent(self, session, trace_config_ctx: LogContext, params):
        trace_config_ctx.request_body = params.chunk

    async def request_end(self, session, trace_config_ctx: LogContext, params):
        trace_config_ctx.response_datetime = datetime.datetime.utcnow()
        trace_config_ctx.elapsed_time = trace_config_ctx.response_datetime - trace_config_ctx.request_datetime
        trace_config_ctx.response_status_code = params.response.status
        trace_config_ctx.response_body = await params.response.read()
        trace_config_ctx.response_headers = {}
        for k, v in params.headers.items():
            trace_config_ctx.response_headers[k] = v
        trace_config_ctx.exception = None
        await self.call_context_handler(trace_config_ctx)

    async def request_exception(self, session, trace_config_ctx: LogContext, params):
        trace_config_ctx.response_datetime = datetime.datetime.utcnow()
        trace_config_ctx.elapsed_time = trace_config_ctx.response_datetime - trace_config_ctx.request_datetime
        trace_config_ctx.response_status_code = None
        trace_config_ctx.response_body = None
        trace_config_ctx.response_headers = None
        trace_config_ctx.exception = ''.join(traceback.format_tb(params.exception.__traceback__))
        await self.call_context_handler(trace_config_ctx)
