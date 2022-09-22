from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Optional, Union, Mapping, Any
from datetime import datetime

from services import server
from services.api import Controller
from services.database import Database
from services.api.utils.responses  import (
    Response,
    ResponseSuccess,
    ResponseFailure
)
from src.models import (
    Empresas,
    Usuarios,
    Produtos,
    ContasPagarReceber,
    Vendas,
    ItensVenda
)
from src.middlewares import (
    AutenticacaoMiddleware,
    ValidacaoCorpoRequisicaoMiddleware
)



database: Database = server.databases.get_database()


class ModelItensVenda:
    def __init__(
        self,
        hash_produto: str,
        quantidade: int
    ) -> None:
        self.hash_produto: str = hash_produto
        self.quantidade: int = quantidade


class ModelVendas:
    def __init__(
        self,
        itens: list[Mapping[str, Any]],
        valor_desconto: float = 0,
        valor_acrescimo: float = 0,
        data_cadastro: datetime = datetime.now(),
        data_alteracao: Optional[datetime] = None,
        obs: Optional[str] = None
    ) -> None:
        self.valor_desconto: float = valor_desconto
        self.valor_acrescimo: float = valor_acrescimo
        self.data_cadastro: str = str(data_cadastro)
        self.data_alteracao: Optional[str] = str(data_alteracao) if data_alteracao else None
        self.obs: Optional[str] = obs

        self.itens: list[ModelItensVenda] = [
            ModelItensVenda(**item)
            for item in itens
        ]



class CrudVendasController(Controller):
    @AutenticacaoMiddleware.apply()
    def get(
        self,
        auth_company: Empresas,
        auth_user: Usuarios
    ) -> Response:
        pass