from .server import Server
from .configs import (
    __API__,
    __DATABASES__,
    __WEB_SOCKET__
)

def init_server() -> Server:
    from typing import Optional, Mapping
    from .database import SingletonDatabases, Databases
    from .websocket import ServerSocket

    options_websocket: Mapping[str, bool] = (__WEB_SOCKET__ or {})

    databases: Databases = \
        SingletonDatabases\
            .get_instance()\
            .append_databases(*__DATABASES__)

    websocket: Optional[ServerSocket] = \
        ServerSocket(
            __API__, options_websocket.get('ASYNC'), 
            options_websocket.get('DEBUG')
        ) \
            if options_websocket.get('ACTIVE') \
            else None

    return Server(__API__, databases, websocket)


server: Server = init_server()


