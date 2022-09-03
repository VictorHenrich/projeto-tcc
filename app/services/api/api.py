from flask import Flask
from flask_restful import Api as ApiFlask
from typing import Any, Mapping, Sequence, Union
from ssl import create_default_context


class Api(ApiFlask):
    __params_app_run: Sequence[str] = 'host', 'port', 'debug'

    def __init__(
        self,
        host: str,
        port: Union[str, int],
        name: str = __name__,
        debug: bool = False,
        is_safe: bool = False,
    ) -> None:
        self.__application: Flask = Flask(name)

        self.__configs: Mapping[str, Any] = {
            'host': host,
            'port': port,
            'debug': debug,
            'is_safe': is_safe 
        }

        super().__init__(app=self.__application)

    @property
    def application(self) -> Flask:
        return self.__app

    @property
    def configs(self) -> Mapping[str, Any]:
        return self.__configs

    def run(self) -> None:
        params: Mapping[str, Any] = {
            prop: value
            for prop, value in self.__configs.items()
            if prop in Api.__params_app_run
        }

        self.__application.run(
            **params,
            ssl_context=\
                create_default_context() \
                if self.__configs['is_safe'] \
                else None
        )

