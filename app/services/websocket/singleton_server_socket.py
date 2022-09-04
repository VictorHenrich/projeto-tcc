from typing import Optional
from . import ServerSocket
from ..api import Api


class SingletonServerSocket:
    __instance: Optional[ServerSocket] = None

    @classmethod
    def get_instance(cls, app: Api, **kwargs) -> ServerSocket:
        if cls.__instance:
            raise Exception('ServerSocket has declared!')

        server_socket: ServerSocket = ServerSocket(app, **kwargs)

        cls.__instance = server_socket

        return server_socket