from . import BuilderDefaultDialect
from .. import Database


class Postgres(BuilderDefaultDialect):
    def __init__(self) -> None:
        super().__init__(
            driver_default="psycopg2", 
            driver_async="asyncpg",
            port=5432
        )

    def build(self) -> Database:
        driver: str = self.driver_default if not self.async_ else self.driver_async

        url: str = \
            f"postgresql+{driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.dbname}"

        return Database(
            url_connection=url,
            name=self.name,
            async_=self.async_,
            debug=self.debug
        )