import logging.config

from fastapi import FastAPI, Depends
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from xps_crypto.incoming_request_log.request_enrichment import inject_body
from xps_crypto.incoming_request_log.middleware import LogMiddleware

from .. import config
from .. import database
from . import middlewares
from . import errors
from . import urls


logging.config.dictConfig(config.LOGGING)


def init_app():
    title = 'XPS CRYPTO'
    prefix_root = '/api/v1'
    application = FastAPI(title=title)
    # middlwares
    application.add_middleware(LogMiddleware, save_model_class=None)
    application.add_middleware(BaseHTTPMiddleware, dispatch=middlewares.catch_exceptions_middleware)
    application.add_middleware(CORSMiddleware, **middlewares.cors_middleware_params)
    # exception handlers (as middlewares)
    application.add_exception_handler(errors.ApiErrorException, errors.api_error_exception_handler)
    # urls
    application.include_router(urls.root_router, prefix=prefix_root, dependencies=[Depends(inject_body)])
    # db bind
    database.db.init_app(application)

    # return
    return application


app = init_app()
