from typing import Protocol, Optional

from fastapi import Request, Response
import sqlalchemy_jsonfield

from .context import LogContext


class LogSaveProtocol(Protocol):
    @classmethod
    async def save_log(cls, log_context: LogContext, request: Optional[Request] = None, response: Optional[Response] = None):
        ...


def incoming_request_model(db):
    class IncomingRequest(LogSaveProtocol):
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

    return IncomingRequest
