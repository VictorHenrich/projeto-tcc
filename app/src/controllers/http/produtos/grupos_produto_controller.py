from datetime import datetime
from typing import Optional
from uuid import UUID

from services import server
from services.database import Database
from services.api import Controller
from src.models import (
    Empresas,
    Usuarios,
    GruposProduto
)
from src.middlewares import (
    AutenticacaoMiddleware,
    ValidacaoCorpoRequisicaoMiddleware,
    ValidacaoParametrosRequisicaoMiddleware
)
from services.api.utils.responses import (
    Response,
    ResponseFailure,
    ResponseSuccess
)



database: Database = server.databases.get_database()


class ModelGruposProduto:
    def __init__(
        self,
        descricao: str,
        data_cadastro: datetime = datetime.now(),
        data_alteracao: Optional[datetime] = None,
        valor_acrescimo: float = 0,
        valor_desconto: float = 0
     ) -> None:
        self.descricao: str = descricao
        self.data_cadastro: str = str(data_cadastro)
        self.data_alteracao: Optional[str] = None if not data_alteracao else str(data_alteracao)
        self.valor_acrescimo: float = valor_acrescimo
        self.valor_desconto: float = valor_desconto



class CrudGruposProdutoController(Controller):
    @AutenticacaoMiddleware.apply()
    def get(
        self,
        auth_company: Empresas,
        auth_user: Usuarios
    ) -> Response:
        try:
            with database.create_session() as session:
                lista_grupos: GruposProduto = \
                    session\
                        .query(GruposProduto)\
                        .filter(
                            GruposProduto.id_empresa == auth_company.id
                        )\
                        .all()

        except Exception as error:
            return ResponseFailure(data=str(error))

        else:
            resposta: list[GruposProduto] = \
                [
                    ModelGruposProduto(
                        descricao=grupo.descricao,
                        data_cadastro=grupo.data_cadastro,
                        valor_acrescimo=grupo.valor_acrescimo,
                        valor_desconto=grupo.valor_desconto
                    ).__dict__

                    for grupo in lista_grupos
                ]

            return ResponseSuccess(data=resposta)

    @AutenticacaoMiddleware.apply()
    @ValidacaoCorpoRequisicaoMiddleware.apply(ModelGruposProduto)
    def post(
        self,
        auth_company: Empresas,
        auth_user: Usuarios,
        body_request: ModelGruposProduto
    ) -> Response:
        try:
            with database.create_session() as session:
                grupo: GruposProduto = GruposProduto()

                grupo.id_empresa = auth_company.id
                grupo.descricao = body_request.descricao
                grupo.data_cadastro = datetime.now()
                grupo.valor_acrescimo = body_request.valor_acrescimo
                grupo.valor_desconto = body_request.valor_desconto

                session.add(grupo)
                session.commit()

        except Exception as error:
            return ResponseFailure(data=str(error))

        else:
            return ResponseSuccess()

    @AutenticacaoMiddleware.apply()
    @ValidacaoCorpoRequisicaoMiddleware.apply(ModelGruposProduto)
    def put(
        self,
        auth_company: Empresas,
        auth_user: Usuarios,
        body_request: ModelGruposProduto,
        hash_grupo: UUID
    ) -> Response:
        try:
            with database.create_session() as session:
                grupo_localizado: GruposProduto = \
                    session\
                        .query(GruposProduto)\
                        .filter(
                            GruposProduto.id_empresa == auth_company.id,
                            GruposProduto.id_uuid == str(hash_grupo)
                        )\
                        .first()

            if not grupo_localizado:
                raise Exception('Grupo de produtos não localizado!')

            grupo_localizado.descricao = body_request.descricao
            grupo_localizado.valor_acrescimo = body_request.valor_acrescimo
            grupo_localizado.valor_desconto = body_request.valor_desconto
            grupo_localizado.data_alteracao = datetime.now()

            session.commit()

        except Exception as error:
            return ResponseFailure(data=str(error))

        else:
            return ResponseSuccess()

    @AutenticacaoMiddleware.apply()
    def delete(
        self,
        auth_company: Empresas,
        auth_user: Usuarios,
        hash_grupo: UUID
    ) -> Response:
        try:
            with database.create_session() as session:
                grupo_localizado: GruposProduto = \
                    session\
                        .query(GruposProduto)\
                        .filter(
                            GruposProduto.id_empresa == auth_company.id,
                            GruposProduto.id_uuid == hash_grupo
                        )\
                        .first()

                if not grupo_localizado:
                    raise Exception('Grupo não localizado!')

                session.delete(grupo_localizado)
                session.commit()

        except Exception as error:
            return ResponseFailure(data=str(error))

        else:
            return ResponseSuccess()






        



