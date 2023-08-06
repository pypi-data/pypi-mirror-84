import socket
import pathlib

from sqlalchemy.engine.url import URL, make_url
from starlette.config import Config
from starlette.datastructures import Secret

config_path = pathlib.Path(__file__).parent.absolute() / ".env"
config = Config(str(config_path))

TESTING = config("TESTING", cast=bool, default=False)

DB_DRIVER = config("DB_DRIVER", default="postgresql")
DB_HOST = config("DB_HOST", default='127.0.0.1')
DB_PORT = config("DB_PORT", cast=int, default=5432)
DB_USER = config("DB_USER", default='xps_crypto')
DB_PASSWORD = config("DB_PASSWORD", cast=Secret, default='xps_crypto')
DB_DATABASE = config("DB_DATABASE", default='xps_crypto')
DB_DSN = config(
    "DB_DSN",
    cast=make_url,
    default=URL(
        drivername=DB_DRIVER,
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_DATABASE,
    ),
)
DB_POOL_MIN_SIZE = config("DB_POOL_MIN_SIZE", cast=int, default=1)
DB_POOL_MAX_SIZE = config("DB_POOL_MAX_SIZE", cast=int, default=16)
DB_ECHO = config("DB_ECHO", cast=bool, default=False)
DB_SSL = config("DB_SSL", default=None)
DB_USE_CONNECTION_FOR_REQUEST = config(
    "DB_USE_CONNECTION_FOR_REQUEST", cast=bool, default=True
)
DB_RETRY_LIMIT = config("DB_RETRY_LIMIT", cast=int, default=1)
DB_RETRY_INTERVAL = config("DB_RETRY_INTERVAL", cast=int, default=1)


ALLOWED_ORIGINS = [
    "*",
]

HOSTNAME = socket.gethostname()

TG_TOKEN = "1190163721:AAFrFlufcFy0EmUNu-Z-GWFuCqWe7fwD_m0"
TG_CHATS = [607015]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] [{0} %(name)s:%(lineno)s] %(message)s'.format(HOSTNAME)
        }
    },
    "handlers": {
        'telegram_handler': {
            'class': 'telegram_log.handler.TelegramHandler',
            'token': TG_TOKEN,
            'chat_ids': TG_CHATS,
            'err_log_name': None,
            'formatter': 'verbose',
        },
        'console_handler': {
            'class': 'logging.StreamHandler',
        },
    },
    "loggers": {
        "telegram": {
            "level": "INFO",
            "handlers": ["telegram_handler", "console_handler"]
        }
    }
}
