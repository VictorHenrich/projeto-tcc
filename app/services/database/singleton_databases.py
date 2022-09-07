from . import Databases
from ..utils.patterns import AbstractSingleton


class SingletonDatabases(AbstractSingleton):
    @classmethod
    def get_instance(cls) -> Databases:
        if cls.instance:
            raise Exception('Instantiates the Databases has declared!')

        databases: Databases = Databases()

        cls.instance = databases

        return databases