from email.policy import default
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Boolean
)
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, date

from services import server
from services.database import Database
from services.database.utils.uuid import create_uuid


database: Database = server.databases.get_database()


class Empresas(database.Model):
    __tablename__ = "empresas"
    id: int = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    id_uuid: str = Column(UUID(True), default=create_uuid, unique=True, nullable=False)
    razao_social: str = Column(String(250), nullable=False)
    cnpj: str = Column(String(250), nullable=False)
    ativo: bool = Column(Boolean, default=True)
    data_cadastro: date = Column(Date, default=datetime.now)
    data_alteracao: date = Column(Date)