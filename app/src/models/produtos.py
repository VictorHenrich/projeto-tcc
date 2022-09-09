from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Boolean,
    ForeignKey,
    DateTime
)
from sqlalchemy.dialects.postgresql import UUID

from services import server
from services.database import Database
from src.models import Empresas, Usuarios
from services.database.utils.uuid import create_uuid


database: Database = server.databases.get_database()


class GruposProduto(database.Model):
    __tablename__: str = "grupos_produto"

    id: int = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    id_uuid: str = Column(UUID(True), default=create_uuid)
    id_empresa: int = Column(Integer, ForeignKey(f"{Empresas.__tablename__}.id"))
    descricao: str = Column(String(255))
    data_cadastro: datetime = Column(DateTime, default=datetime.now)
    valor_acrescimo: float = Column(Float, default=0, nullable=False)
    valor_desconto: float = Column(Float, default=0, nullable=False)


class SubGruposProduto(database.Model):
    __tablename__: str = "grupos_produto"

    id: int = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    id_uuid: str = Column(UUID(True), default=create_uuid)
    id_empresa: int = Column(Integer, ForeignKey(f"{Empresas.__tablename__}.id"), nullable=False)
    id_grupo: int = Column(Integer, ForeignKey(f"{GruposProduto.__tablename__}.id"))
    descricao: str = Column(String(255))
    data_cadastro: datetime = Column(DateTime, default=datetime.now)
    valor_acrescimo: float = Column(Float, default=0, nullable=False)
    valor_desconto: float = Column(Float, default=0, nullable=False)


class Produtos(database.Model):
    __tablename__: str = "produtos"

    id: int = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    id_uuid: str = Column(UUID(True), default=create_uuid, nullable=False, unique=True)
    id_empresa: int = Column(Integer, ForeignKey(f"{Empresas.__tablename__}.id"), nullable=False)
    id_usuario_alteracao: int = Column(Integer, ForeignKey(f"{Usuarios.__tablename__}.id"))
    id_grupo: int = Column(Integer, ForeignKey(f"{GruposProduto.__tablename__}.id"))
    descricao: str = Column(String(255), nullable=False)
    codigo_barras: str = Column(String(255))
    data_cadastro: datetime = Column(DateTime, default=datetime.now)
    data_alteracao: datetime = Column(DateTime)
    valor_venda: float = Column(Float, default=0)
    porcentagem_lucro: float = Column(Float, default=0)
    valor_custo: float = Column(Float, default=0)
    ativo: bool = Column(Boolean, default=True, nullable=False)





