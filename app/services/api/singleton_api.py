from ctypes import Union
from typing import Optional
from . import Api


class SingletonApi:
    __instance: Optional[Api] = None

    @classmethod
    def get_instance(
        cls,
        host: str,
        port: Union[str, int],
        name: str = __name__,
        debug: bool = False,
        is_safe: bool = False,
    ) -> Api:
        if cls.__instance:
            raise Exception('Instantiates the Api has declared!')

        api: Api = Api(host, port, name, debug, is_safe)

        cls.__instance = api

        return api