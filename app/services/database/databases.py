from __future__ import annotations
from typing import Mapping, Optional, Sequence
from . import Database


class Databases:
    def __init__(self) -> None:
        self.__bases: Mapping[str, Database] = dict()

    @property
    def bases(self) -> Mapping[str, Database]:
        return self.__bases

    def append_databases(self, *databases: Sequence[Database]) -> Databases:
        try:
            for database in databases:
                self.__bases[database.name] = database

            return self

        except Exception:
            raise Exception('Failure in insert the databases!')

    def remove_databases(self, *namebases: Sequence[str]) -> Databases:
        try:
            for namebase in namebases:
                del self.__bases[namebase]

            return self

        except:
            raise Exception('Failure in remove the bases!')

    def get_database(self, name: Optional[str] = None) -> Database:
        try:
            return self.__bases.get('main') or list(self.__bases.values())[0] \
                    if not name \
                    else self.__bases[name]
        except IndexError:
            raise Exception('There is no database allocated in this instantiation')

        except KeyError:
            raise Exception('Database not found!')

        except:
            raise Exception('Failure in get Database!')

    def migrate_all(self) -> Databases:
        try:
            for database in self.__bases.items():
                database.migrate()

            return self
            
        except:
            raise Exception('Failure in migrations!')

