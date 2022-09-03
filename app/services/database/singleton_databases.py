from typing import Optional
from . import Databases


class SingletonDatabases:
    __instance: Optional[Databases] = None

    @classmethod
    def get_instance(cls) -> Databases:
        if cls.__instance:
            raise Exception('Instantiates the Databases has declared!')

        databases: Databases = Databases()

        cls.__instance = databases

        return databases