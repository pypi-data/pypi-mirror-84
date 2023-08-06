from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .base import ApiErrorException


async def api_error_exception_handler(request: Request, exc: ApiErrorException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(exc.error),
    )
