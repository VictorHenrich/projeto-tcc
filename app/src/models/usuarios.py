from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Boolean,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, date

from services import server
from services.database import Database
from services.database.utils.uuid import create_uuid
from . import empresas


database: Database = server.databases.get_database()


class Usuarios(database.Model):
    __tablename__ = "usuarios"
    id: int = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    id_uuid: str = Column(UUID(False), default=create_uuid, unique=True, nullable=False)
    id_empresa: int = Column(Integer, ForeignKey(f"{empresas.Empresas.__tablename__}.id"))
    email: str = Column(String(250))
    senha: str = Column(String(50))
    ativo: bool = Column(Boolean, default=True)
    data_cadastro: date = Column(Date, default=datetime.now)
    data_alteracao: date = Column(Date) 
