from typing import List

from gino.ext.starlette import Gino

from . import config

db = Gino(
    dsn=config.DB_DSN,
    pool_min_size=config.DB_POOL_MIN_SIZE,
    pool_max_size=config.DB_POOL_MAX_SIZE,
    echo=config.DB_ECHO,
    ssl=config.DB_SSL,
    use_connection_for_request=config.DB_USE_CONNECTION_FOR_REQUEST,
    retry_limit=config.DB_RETRY_LIMIT,
    retry_interval=config.DB_RETRY_INTERVAL,
)


async def db_force_init():
    db_config = db.config
    await db.set_bind(
        db_config["dsn"],
        echo=db_config["echo"],
        min_size=db_config["min_size"],
        max_size=db_config["max_size"],
        ssl=db_config["ssl"],
        **db_config["kwargs"]
    )


def get_app_models_modules() -> List:
    return [
    ]
