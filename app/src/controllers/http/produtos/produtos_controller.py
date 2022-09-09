from typing import Optional, Mapping, Any
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
from src.middlewares import AutenticacaoMiddleware, ValidacaoCorpoRequisicaoMiddleware
from src.models import Usuarios, Empresas, Produtos, GruposProduto


database: Database = \
    server\
        .databases\
        .get_database()


class ModelProduto:
    def __init__(
        self,
        descricao: str,
        codigo_barras: Optional[str] = None,
        data_cadastro: datetime = datetime.now(),
        data_alteracao: Optional[datetime] = None,
        valor_venda: float = 0,
        porcentagem_lucro: float = 0,
        valor_custo: float =  0,
        ativo: bool = True,
        grupo: Optional[UUID] = None
    ) -> None:
        self.descricao: str = descricao
        self.codigo_barras: Optional[str] = codigo_barras
        self.data_cadastro: str = str(data_cadastro)
        self.data_alteracao: Optional[str] = None if not data_alteracao else str(data_alteracao)
        self.valor_venda: float = valor_venda
        self.porcentagem_lucro: float = porcentagem_lucro
        self.valor_custo: float = valor_custo
        self.ativo: bool = ativo
        self.grupo: Optional[str] = None if not grupo else str(grupo)



class ProdutosController(Controller):
    @AutenticacaoMiddleware.apply()
    def get(
        self, 
        auth_user: Usuarios, 
        auth_company: Empresas
    ) -> Response:
        try:
            with database.create_session() as session:
                lista_produtos: list[Produtos] = \
                    session\
                        .query(Produtos)\
                        .filter(
                            Produtos.id_empresa == auth_company.id
                        )\
                        .all()

        except Exception as error:
            return ResponseFailure(data=str(error))

        else:
            resposta: list[Mapping[str, Any]] = \
                [
                    {
                        **ModelProduto(
                            descricao=produto.descricao,
                            codigo_barras=produto.codigo_barras,
                            data_cadastro=produto.data_cadastro,
                            data_alteracao=produto.data_alteracao,
                            valor_venda=produto.valor_venda,
                            porcentagem_lucro=produto.porcentagem_lucro,
                            valor_custo=produto.valor_custo,
                            ativo=produto.ativo
                        ).__dict__,
                        'id_uuid': produto.id_uuid
                    }

                    for produto in lista_produtos
                ]

            return ResponseSuccess(data=resposta)

    @AutenticacaoMiddleware.apply()
    @ValidacaoCorpoRequisicaoMiddleware.apply(ModelProduto)
    def post(
        self, 
        auth_user: Usuarios, 
        auth_company: Empresas, 
        body_request: ModelProduto
    ) -> Response:
        try:
            with database.create_session() as session:

                produto: Produtos = Produtos()

                produto.id_empresa = auth_company.id
                produto.id_usuario_alteracao = auth_user.id
                produto.descricao = body_request.descricao
                produto.codigo_barras = body_request.codigo_barras
                produto.valor_venda = body_request.valor_venda
                produto.valor_custo = body_request.valor_custo
                produto.porcentagem_lucro = body_request.porcentagem_lucro

                if body_request.grupo:
                    grupo_localizado: GruposProduto = \
                        session\
                            .query(GruposProduto)\
                            .filter(
                                GruposProduto.id_empresa == auth_company.id,
                                GruposProduto.id_uuid == body_request.grupo
                            )

                    if not grupo_localizado:
                        raise Exception('Falha ao localizar grupo de produtos!')


                    produto.id_grupo = grupo_localizado.id

                session.add(produto)
                session.commit()

        except Exception as error:
            return ResponseFailure(data=str(error))

        else:
            return ResponseSuccess()

    @AutenticacaoMiddleware.apply()
    @ValidacaoCorpoRequisicaoMiddleware.apply(ModelProduto)
    def put(
        self,
        auth_user: Usuarios, 
        auth_company: Empresas, 
        body_request: ModelProduto,
        hash_produto: UUID
    ) -> Response:
        try:
            with database.create_session() as session:
                produto_localizado: Produtos = \
                    session\
                        .query(Produtos)\
                        .filter(
                            Produtos.id_empresa == auth_company.id,
                            Produtos.id_uuid == str(hash_produto)
                        )\
                        .first()


                if not produto_localizado:
                    raise Exception('Produto não localizado!')

                
                produto_localizado.id_empresa = auth_company.id
                produto_localizado.id_usuario_alteracao = auth_user.id
                produto_localizado.descricao = body_request.descricao
                produto_localizado.codigo_barras = body_request.codigo_barras
                produto_localizado.valor_venda = body_request.valor_venda
                produto_localizado.valor_custo = body_request.valor_custo
                produto_localizado.porcentagem_lucro = body_request.porcentagem_lucro

                if body_request.grupo:
                    grupo_localizado: GruposProduto = \
                        session\
                            .query(GruposProduto)\
                            .filter(
                                GruposProduto.id_empresa == auth_company.id,
                                GruposProduto.id_uuid == body_request.grupo
                            )

                    if not grupo_localizado:
                        raise Exception('Falha ao localizar grupo de produtos!')


                    produto_localizado.id_grupo = grupo_localizado.id

                session.commit()

        except Exception as error:
            return ResponseFailure(data=str(error))

        else:
            return ResponseSuccess()

    @AutenticacaoMiddleware.apply()
    def delete(
        self,
        auth_user: Usuarios,
        auth_company: Empresas,
        hash_produto: UUID
    ) -> Response:
        try:
            with database.create_session() as session:
                produto_localizado: Produtos =\
                    session\
                        .query(Produtos)\
                        .filter(
                            Produtos.id_empresa == auth_company.id,
                            Produtos.id_uuid == str(hash_produto)
                        )\
                        .first()

                if not produto_localizado:
                    raise Exception('Produto não foi localizado!')

                session.delete(produto_localizado)
                session.commit()

        except Exception as error:
            return ResponseFailure(data=str(error))

        else:
            return ResponseSuccess()

