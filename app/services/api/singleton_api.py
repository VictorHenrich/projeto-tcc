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
        **kwargs
    ) -> Api:
        if cls.__instance:
            raise Exception('Instantiates the Api has declared!')

        api: Api = Api(host, port, **kwargs)

        cls.__instance = api

        return api