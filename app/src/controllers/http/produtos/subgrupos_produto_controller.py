from uuid import UUID
from datetime import datetime
from typing import Any, Optional, Mapping, Tuple

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
    GruposProduto,
    SubGruposProduto
)
from src.middlewares import (
    AutenticacaoMiddleware,
    ValidacaoCorpoRequisicaoMiddleware
)


database: Database = server.databases.get_database()


class ModelSubgrupo:
    def __init__(
        self,
        descricao: str,
        uuid_grupo: str,
        data_cadastro: datetime = datetime.now,
        data_alteracao: Optional[datetime] = None,
        valor_acrescimo: float = 0,
        valor_desconto: float = 0
    ) -> None:
        self.descricao: str = descricao
        self.uuid_grupo: str = uuid_grupo
        self.data_cadastro: str = str(data_cadastro)
        self.data_alteracao: Optional[str] = str(data_alteracao) if data_alteracao else None
        self.valor_acrescimo: float = valor_acrescimo
        self.valor_desconto: float = valor_desconto



class CrudSubgruposProdutoController(Controller):
    @AutenticacaoMiddleware.apply()
    def get(
        self,
        auth_company: Empresas,
        auth_user: Usuarios
    ) -> Response:
        try:
            with database.create_session() as session:
                lista_grupos_e_subgrupos: list[Tuple[SubGruposProduto, GruposProduto]] = \
                    session\
                        .query(SubGruposProduto, GruposProduto)\
                        .join(
                            SubGruposProduto.id_grupo == GruposProduto.id
                        )\
                        .filter(
                            SubGruposProduto.id_empresa == auth_company.id
                        )\
                        .all()

        except Exception as error:
            return ResponseFailure(data=str(error))

        else:
            resposta: list[Mapping[str, Any]] =\
                [
                    {
                        **ModelSubgrupo(
                            descricao=subgrupo.descricao,
                            uuid_grupo=grupo.id_uuid,
                            data_cadastro=subgrupo.data_cadastro,
                            data_alteracao=subgrupo.data_alteracao,
                            valor_acrescimo=subgrupo.valor_acrescimo,
                            valor_desconto=subgrupo.valor_desconto
                        ).__dict__,
                        "id_uuid": subgrupo.id_uuid
                    }
                    for subgrupo, grupo in lista_grupos_e_subgrupos
                ]


            return ResponseSuccess(data=resposta)

    @AutenticacaoMiddleware.apply()
    @ValidacaoCorpoRequisicaoMiddleware.apply(ModelSubgrupo)
    def post(
        self,
        auth_company: Empresas,
        auth_user: Usuarios,
        body_request: ModelSubgrupo
    ) -> Response:
        try:
            with database.create_session() as session:

                grupo_localizado: GruposProduto = \
                    session\
                        .query(GruposProduto)\
                        .filter(
                            GruposProduto.id_empresa == auth_company.id,
                            GruposProduto.id_uuid == body_request.uuid_grupo
                        )\
                        .first()

                if not grupo_localizado:
                    raise Exception('Grupo de produtos não localizado!')


                subgrupo: SubGruposProduto = SubGruposProduto()
                subgrupo.id_empresa = auth_company.id
                subgrupo.id_grupo = grupo_localizado.id
                subgrupo.descricao = body_request.descricao
                subgrupo.valor_acrescimo =  body_request.valor_acrescimo
                subgrupo.valor_desconto = body_request.valor_desconto
                
                session.add(subgrupo)
                session.commit()

        except Exception as error:
            return ResponseFailure(data=str(error))

        else:
            return ResponseSuccess()

    @AutenticacaoMiddleware.apply()
    @ValidacaoCorpoRequisicaoMiddleware.apply()
    def put(
        self,
        auth_company: Empresas,
        auth_user: Usuarios,
        body_request: ModelSubgrupo,
        hash_subgrupo: UUID   
    ) -> Response:
        try:
            with database.create_session() as session:
                subgrupo_localizado: SubGruposProduto = \
                    session\
                        .query(SubGruposProduto)\
                        .filter(
                            SubGruposProduto.id_empresa == auth_company.id,
                            SubGruposProduto.id_uuid == str(hash_subgrupo)
                        )\
                        .first()

                if not subgrupo_localizado:
                    raise Exception('Subgrupo de produtos não localizado!')


                grupo_localizado: GruposProduto = \
                    session\
                        .query(GruposProduto)\
                        .filter(
                            GruposProduto.id_empresa == auth_company.id,
                            GruposProduto.id_uuid == body_request.uuid_grupo
                        )\
                        .first()

                if not grupo_localizado:
                    raise Exception('Grupo de produtos não localizado!')


                subgrupo_localizado.id_grupo = grupo_localizado.id
                subgrupo_localizado.descricao = body_request.descricao
                subgrupo_localizado.data_alteracao = datetime.now()
                subgrupo_localizado.valor_acrescimo = body_request.valor_acrescimo
                subgrupo_localizado.valor_desconto = body_request.valor_desconto
                
                session.add(subgrupo_localizado)
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
        hash_subgrupo: UUID
    ) -> Response:
        try:
            with database.create_session() as session:
                subgrupo_localizado: SubGruposProduto = \
                    session\
                        .query(SubGruposProduto)\
                        .filter(
                            SubGruposProduto.id_empresa == auth_company.id,
                            SubGruposProduto.id_uuid == str(hash_subgrupo)
                        )\
                        .first()

                if not subgrupo_localizado:
                    raise Exception('Subgrupo de produtos não localizado')

                session.delete(subgrupo_localizado)
                session.commit()

        except Exception as error:
            return ResponseFailure(data=str(error))

        else:
            return ResponseSuccess()

        