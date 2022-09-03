from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Union

from .. import Database


@dataclass
class BuilderDefaultDialect:
    host: Optional[str] = None
    port: Optional[Union[str, int]] = None
    dbname: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    debug: bool = False
    has_async: bool = False
    name: str = "main"
    driver_default: str = ""
    driver_async: str = ""

    def set_host(self, host: str) -> BuilderDefaultDialect:
        self.host = host

        return self

    def set_port(self, port: Union[str, int]) -> BuilderDefaultDialect:
        self.port = port
        
        return self

    def set_dbname(self, dbname: str) -> BuilderDefaultDialect:
        self.dbname = dbname

        return self

    def set_credentials(self, username: str, password: str) -> BuilderDefaultDialect:
        self.username = username
        self.password = password

        return self

    def set_debug(self, debug: bool) -> BuilderDefaultDialect:
        self.debug = debug

        return self

    def set_has_async(self, has_async: bool) -> BuilderDefaultDialect:
        self.has_async = has_async

        return self

    def set_name(self, name: str) -> BuilderDefaultDialect:
        self.name = name

        return self
    
    def set_driver_default(self, driver: str) -> BuilderDefaultDialect:
        self.driver_default = driver

        return self

    def set_driver_async(self, driver: str) -> BuilderDefaultDialect:
        self.driver_async = driver

        return self

    def build(self) -> Database:
        raise NotImplementedError('Method builder not implemented!')