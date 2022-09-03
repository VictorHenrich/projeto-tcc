from .server import Server
from .configs import (
    __API__,
    __DATABASES__
)

def init_server() -> Server:
    from .database import SingletonDatabases, Databases

    databases: Databases = \
        SingletonDatabases\
            .get_instance()\
            .append_databases(*__DATABASES__)

    return Server(__API__, databases)


server: Server = init_server()


