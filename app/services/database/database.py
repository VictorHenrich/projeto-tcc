from sqlalchemy.engine import create_engine, Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm.session import Session, sessionmaker
from sqlalchemy.orm.decl_api import declarative_base, DeclarativeMeta
from typing import Union, Type
import asyncio


class Database:
    def __init__(
        self,
        url_connection: str,
        name: str = 'main',
        async_: bool = False,
        debug: bool = False
    ) -> None:
        self.__engine: Union[Engine, AsyncEngine] = \
                create_engine(url_connection, echo=debug) \
                if not async_ \
                else create_async_engine(url_connection, echo=debug)

        self.__Model: Type[DeclarativeMeta] = declarative_base(self.__engine)

        self.__name: str = name

    @property
    def engine(self) -> Union[Engine, AsyncEngine]:
        return self.__engine

    @property
    def Model(self) -> Type[DeclarativeMeta]:
        return self.__Model

    @property
    def name(self) -> str:
        return self.__name

    def migrate(self, drop_tables: bool = False) -> None:
        if type(self.__engine) is not AsyncEngine:
            self.__migrate_default(drop_tables)

        else:
            asyncio.run(self.__migrate_async())

    def __migrate_default(self, drop_all: bool) -> None:
        if drop_all:
            self.__Model.metadata.drop_all(self.__engine)

        self.__Model.metadata.create_all(self.__engine)

    async def __migrate_async(self, drop_all: bool) -> None:
        with self.__engine.begin() as connection:
            if drop_all:
                connection.run_async(self.__Model.metadata.drop_all)

            connection.run_sync(self.__Model.metadata.create_all)

    def create_session(self, **kwargs) -> Union[Session, AsyncSession]:
        return sessionmaker(
            bind= self.__engine,
            class_= Session if type(self.__engine) is not AsyncEngine else AsyncSession,
            **kwargs
        )()