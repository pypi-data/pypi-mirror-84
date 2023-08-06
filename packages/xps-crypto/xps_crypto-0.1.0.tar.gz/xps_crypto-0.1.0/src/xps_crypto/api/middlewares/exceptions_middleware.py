import logging

from starlette.requests import Request


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        tg = logging.getLogger("telegram")
        if tg:
            tg.exception("xps_proxy request exception.")
        raise
