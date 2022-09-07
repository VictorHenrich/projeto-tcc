from typing import Optional, Union
from . import Api
from ..utils.patterns import AbstractSingleton


class SingletonApi(AbstractSingleton):
    @classmethod
    def get_instance(
        cls,
        host: str,
        port: Union[str, int],
        **kwargs
    ) -> Api:
        if cls.instance:
            raise Exception('Instantiates the Api has declared!')

        api: Api = Api(host, port, **kwargs)

        cls.instance = api

        return api