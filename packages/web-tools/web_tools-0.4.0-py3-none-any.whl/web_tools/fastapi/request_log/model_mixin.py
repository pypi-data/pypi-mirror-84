from __future__ import annotations

from typing import Optional

from fastapi import Request, Response
import sqlalchemy_jsonfield

from .context import LogContext


class SaveLogMixin:
    @classmethod
    async def save_log(cls,
                       log_context: LogContext,
                       request: Optional[Request] = None,
                       response: Optional[Response] = None):
        raise NotImplemented


def incoming_request_model(db):
    class IncomingRequest(SaveLogMixin):
        id = db.Column(db.BigInteger(), primary_key=True)

        request_datetime = db.Column(db.DateTime(), index=True)
        request_url = db.Column(db.Unicode(), index=True)
        request_method = db.Column(db.Unicode(), index=True)
        request_headers = db.Column(
            sqlalchemy_jsonfield.JSONField(enforce_string=True, enforce_unicode=False),
            nullable=True
        )
        request_body = db.Column(db.LargeBinary(), nullable=True)

        response_datetime = db.Column(db.DateTime(), index=True, nullable=True)
        response_status_code = db.Column(db.Integer(), index=True, nullable=True)
        response_headers = db.Column(
            sqlalchemy_jsonfield.JSONField(enforce_string=True, enforce_unicode=False),
            nullable=True
        )
        response_body = db.Column(db.LargeBinary(), nullable=True)

        elapsed_time = db.Column(db.Interval(), nullable=True)
        exception = db.Column(db.Unicode(), nullable=True)

        def __init__(self,
                     log_context: LogContext,
                     request: Optional[Request] = None,
                     response: Optional[Response] = None):
            self.request_datetime = log_context.request_datetime
            self.request_url = log_context.request_url
            self.request_method = log_context.request_method
            self.request_headers = log_context.request_headers
            self.request_body = log_context.request_body
            self.response_datetime = log_context.response_datetime
            self.response_status_code = log_context.response_status_code
            self.response_headers = log_context.response_headers
            self.response_body = log_context.response_body
            self.elapsed_time = log_context.elapsed_time
            self.exception = log_context.exception

        @classmethod
        async def save_log(cls,
                           log_context: LogContext,
                           request: Optional[Request] = None,
                           response: Optional[Response] = None):
            record = cls(log_context, request=request, response=response)
            # noinspection PyUnresolvedReferences
            await record.create()

    return IncomingRequest
