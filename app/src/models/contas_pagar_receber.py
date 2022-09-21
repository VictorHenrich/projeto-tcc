from datetime import datetime, date
from typing import Sequence
from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Date
)
from sqlalchemy.dialects.postgresql import UUID

from services import server
from services.database import Database
from src.models import Empresas, Usuarios
from services.database.utils.uuid import create_uuid



database: Database = server.databases.get_database()


class ContasPagarReceber(database.Model):
    tipos_conta: Sequence[str] = "PAG", "REC"

    __tablename__: str = "contas_receber_pagar"
    id: int = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    id_uuid: str = Column(UUID(False), unique=True, nullable=False, default=create_uuid)
    id_empresa: int = Column(Integer, ForeignKey(f"{Empresas.__tablename__}.id"))
    id_usuario_alt: int = Column(Integer, ForeignKey(f"{Usuarios.__tablename__}.id"))
    valor: float = Column(Float, nullable=0, default=0)
    obs: str = Column(String(300))
    data_documento: date = Column(Date)
    data_cadastro: datetime = Column(DateTime, default=datetime.now)
    data_alteracao: datetime = Column(DateTime)
    tipo: str = Column(String(10), nullable=False)