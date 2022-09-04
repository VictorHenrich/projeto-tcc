from socketio import AsyncServer, Server, WSGIApp, ASGIApp
from services.api import Api
from typing import Type, Union

from . import Controller, AsyncController


class ServerSocket:
    def __init__(
        self,
        app: Api,
        debug: bool = False,
        async_: bool = False
    ):
        self.__socket: Union[Server, AsyncServer] = \
            Server(logger=debug, engineio_logger=debug) \
                if not async_ \
                else AsyncServer(logger=debug, engineio_logger=debug)

        self.__api: Api = app

        self.__app: WSGIApp = \
            WSGIApp(self.__socket, wsgi_app=self.__api.application.wsgi_app) \
                if not async_ \
                else ASGIApp(self.__socket, other_asgi_app=self.__api.application.wsgi_app)

    @property
    def socket(self) -> Union[Server, AsyncServer]:
        return self.__socket

    @property
    def app(self) -> Union[WSGIApp, ASGIApp]:
        return self.__app

    def run(self) -> None:
        classes: list[Type[Union[Controller, AsyncController]]] = \
            Controller.__subclasses__() + AsyncController.__subclasses__()

        for controller in classes:
            self.__socket.register_namespace(controller(controller.event_name))

        self.__api.run()

        