from __future__ import annotations
from dataclasses import dataclass
from typing import Union
from . import Api
from ..utils.patterns import AbstractBuilder
from uuid import uuid4



@dataclass
class BuilderApi(AbstractBuilder):
    host: str = "localhost"
    port: Union[str, int] = 5000
    debug: bool = False
    security: bool = False
    secret_key: bool = str(uuid4())

    def set_host(self, host: str) -> BuilderApi:
        self.host = host

        return self

    def set_port(self, port: Union[str, int]) -> BuilderApi:
        self.port = port

        return self

    def set_debug(self, debug: bool) -> BuilderApi:
        self.debug = debug

        return self

    def set_security(self, has_save: bool) -> BuilderApi:
        self.security = has_save

        return self

    def set_secret_key(self, secret_key: str) -> BuilderApi:
        self.secret_key = secret_key

        return self

    def build(self) -> Api:
        return Api(
            host=self.host,
            port=self.port,
            secret_key=self.secret_key,
            debug=self.debug,
            is_safe=self.security
        )
