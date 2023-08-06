import sqlalchemy_jsonfield

from .context import LogContext


def outgoing_request_model(db):
    class OutgoingRequest:
        id = db.Column(db.BigInteger(), primary_key=True)
        request_datetime = db.Column(db.DateTime(), index=True, nullable=False)
        request_url = db.Column(db.Unicode(), index=True, nullable=False)
        request_method = db.Column(db.Unicode(), index=True, nullable=False)
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

        @classmethod
        async def save_log(cls, log_context: LogContext):
            log_record = cls()
            # noinspection PyUnresolvedReferences
            log_record.__values__.update(**log_context.as_dict())
            # noinspection PyUnresolvedReferences
            await log_record.create()

    return OutgoingRequest
