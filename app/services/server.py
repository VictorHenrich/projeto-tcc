from typing import Any, Callable, Coroutine, Optional
import asyncio

from .api import Api
from .database import Databases
from .websocket import ServerSocket



class Server:
    def __init__(
        self, 
        api: Api, 
        databases: Databases,
        websocket: Optional[ServerSocket] = None
    ) -> None:
        self.__api: Api = api
        self.__databases: Databases = databases
        self.__websocket: Optional[ServerSocket] = websocket
        self.__initial_functions: list[Callable] = []

    @property
    def api(self) -> Api:
        return self.__api

    @property
    def databases(self) -> Databases:
        return self.__databases

    @property
    def websocket(self) -> ServerSocket:
        return self.__websocket
        
    def start(self, function: Callable[[None], Any]) -> Callable[[None], Any]:
        self.__initial_functions.append(function)

        def wrapper() -> Any:
            return function()

        return wrapper

    def start_server(self) -> None:
        for function in self.__initial_functions:
            result: Optional[Coroutine] = function()

            if isinstance(result, Coroutine):
                asyncio.run(result)

