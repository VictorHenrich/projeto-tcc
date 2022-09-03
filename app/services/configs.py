from .api import Api, BuilderApi
from .database import Database
from .database.dialects import Postgres

__API__: Api = \
    BuilderApi() \
        .set_host('localhost') \
        .set_port(3333) \
        .set_debug(True) \
        .set_security(False) \
        .build()

__DATABASES__: list[Database] = [
    Postgres() \
        .set_host('localhost') \
        .set_dbname('banco_teste') \
        .set_credentials('postgres', '1234') \
        .set_debug(True) \
        .set_has_async(False) \
        .build()
]