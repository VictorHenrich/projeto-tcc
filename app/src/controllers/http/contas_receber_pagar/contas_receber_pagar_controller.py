from typing import Any, Optional, Mapping
from datetime import datetime
from uuid import UUID

from services import server
from services.database import Database
from services.api import Controller
from services.api.utils.responses import (
    Response,
    ResponseFailure,
    ResponseSuccess
)
from src.models import (
    Empresas,
    Usuarios,
    ContasPagarReceber
)
from src.middlewares import (
    AutenticacaoMiddleware,
    ValidacaoCorpoRequisicaoMiddleware
)



database: Database = server.databases.get_database()


class ModelContaPagarReceber:
    def __init__(
        self,
        valor: float,
        tipo: str,
        data_cadastro: datetime = datetime.now(),
        data_documento: Optional[datetime] = None,
        data_alteracao: Optional[datetime] = None,
        obs: Optional[str] = None
    ) -> None:
        tipo_conta, = [
            tipo_
            for tipo_ in ContasPagarReceber.tipos_conta
            if tipo.upper() in ContasPagarReceber.tipos_conta
        ]

        self.valor: float = valor
        self.tipo: str = tipo_conta
        self.data_cadastro: str = str(data_cadastro)
        self.data_documento: Optional[str] = str(data_documento) if data_documento else None
        self.data_alteracao: Optional[str] = str(data_alteracao) if data_alteracao else None
        self.obs: Optional[str] = obs



class CrudContasReceberPagarController(Controller):
    @AutenticacaoMiddleware.apply()
    def get(
        self, 
        auth_company: Empresas,
        auth_user: Usuarios
    ) -> Response:
        try:
            with database.create_session() as session:
                lista_contas_pagar_receber: list[ContasPagarReceber] = \
                    session\
                        .query(ContasPagarReceber)\
                        .filter(
                            ContasPagarReceber.id_empresa == auth_company.id
                        )\
                        .all()


        except Exception as error:
            return ResponseFailure(data=str(error))

        else:
            resposta: list[Mapping[str, Any]] = \
                [
                    {
                        **ModelContaPagarReceber(
                            valor=conta.valor,
                            tipo=conta.tipo,
                            data_cadastro=conta.data_cadastro,
                            data_alteracao=conta.data_alteracao,
                            data_documento=conta.data_documento,
                            obs=conta.obs
                        ).__dict__,

                        "id_uuid": conta.id_uuid
                    }
                    for conta in lista_contas_pagar_receber
                ]

            return ResponseSuccess(data=resposta)

    @AutenticacaoMiddleware.apply()
    @ValidacaoCorpoRequisicaoMiddleware.apply(ModelContaPagarReceber)
    def post(
        self,
        auth_company: Empresas,
        auth_user: Usuarios,
        body_request: ModelContaPagarReceber
    ) -> Response:
        try:
            with database.create_session() as session:
                conta_pagar_receber: ContasPagarReceber = ContasPagarReceber()
                conta_pagar_receber.id_empresa = auth_company.id
                conta_pagar_receber.id_usuario_alt = auth_user.id
                conta_pagar_receber.tipo = body_request.tipo
                conta_pagar_receber.valor = body_request.valor
                conta_pagar_receber.data_documento = body_request.data_documento
                
                session.add(conta_pagar_receber)
                session.commit()

        except Exception as error:
            return ResponseFailure(data=str(error))

        else:
            return ResponseSuccess()
