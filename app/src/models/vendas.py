from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    DateTime,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from typing import Optional

from services import server
from services.database import Database
from services.database.utils.uuid import create_uuid
from src.models import (
    Empresas,
    Usuarios,
    Produtos
)


database: Database = server.databases.get_database()


class Vendas(database.Model):
    __tablename__: str = "vendas"

    id: int = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    id_uuid: str = Column(UUID(False), nullable=False, unique=True, default=create_uuid)
    id_empresa: int = Column(Integer, ForeignKey(f"{Empresas.__tablename__}.id"), nullable=False)
    id_usuario_alteracao: Optional[int] = Column(Integer, ForeignKey(f"{Usuarios.__tablename__}.id"))
    valor_total: float = Column(Float, default=0, nullable=False)
    valor_desconto: float = Column(Float, default=0, nullable=False)
    valor_acrescimo: float = Column(Float, default=0, nullable=False)
    data_cadastro: datetime = Column(DateTime, default=datetime.now, nullable=False)
    data_alteracao: Optional[datetime] = Column(DateTime)
    obs: Optional[str] = Column(String(500))


class ItensVenda(database.Model):
    __tablename__: str = "itens_venda"

    id_uuid: str = Column(UUID(False), nullable=False, unique=True, default=create_uuid)
    id_empresa: int = Column(Integer, ForeignKey(f"{Empresas.__tablename__}.id"), nullable=False)
    id_produto: int = Column(Integer, ForeignKey(f"{Produtos.__tablename__}.id"), nullable=False, primary_key=True)
    id_venda: int = Column(Integer, ForeignKey(f"{Vendas.__tablename__}.id"), nullable=False, primary_key=True)




