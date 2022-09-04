from typing import Optional
from datetime import datetime
from uuid import UUID

from src.models import Usuarios, Empresas
from services.database import Database
from services import server
from services.api import Controller
from services.api.utils.responses import (
    Response,
    ResponseFailure,
    ResponseSuccess
)
from src.middlewares import (
    AutenticacaoMiddleware,
    ValidacaoCorpoRequisicaoMiddleware,
    ValidacaoParametrosRequisicaoMiddleware
)


database: Database = server.databases.get_database()


class VisualizacaoUsuario:
    def __init__(
        self,
        email: Optional[str] = None,
        ativo: bool = True,
        data_cadastro: Optional[datetime] = None,
        data_alteracao: Optional[datetime] = None
    ) -> None:
        self.email: Optional[str] = email
        self.ativo: bool = ativo
        self.data_cadastro: Optional[str] = None if not data_cadastro else str(data_cadastro)
        self.data_alteracao: Optional[str] = None if not data_alteracao else str(data_alteracao)


class CadastroUsuario:
    def __init__(
        self,
        email: str,
        senha: str,
        ativo: bool = True
    ) -> None:
        self.email: str = email
        self.senha: str = senha
        self.ativo: bool = ativo


class CrudUsuariosController(Controller):
    @AutenticacaoMiddleware.apply()
    def get(
        self, 
        auth_user: Usuarios, 
        auth_company: Empresas
    ) -> Response:
        try:
            with database.create_session() as session:
                lista_usuarios: list[Usuarios] = \
                    session\
                        .query(Usuarios)\
                        .filter(Usuarios.id_empresa == auth_company.id)\
                        .all()

        except Exception as error:
            return ResponseFailure(data=str(error))

        else:
            resposta: list[dict] = [
                VisualizacaoUsuario(
                    email=usuario.email,
                    ativo=usuario.ativo,
                    data_cadastro=usuario.data_cadastro,
                    data_alteracao=usuario.data_alteracao
                ).__dict__

                for usuario in lista_usuarios
            ]

            return ResponseSuccess(data=resposta)

    @AutenticacaoMiddleware.apply()
    @ValidacaoCorpoRequisicaoMiddleware.apply(CadastroUsuario)
    def post(
        self, 
        auth_user: Usuarios, 
        auth_company: Empresas, 
        body_request: CadastroUsuario
    ) -> Response:
        try:
            with database.create_session() as session:
                usuario: Usuarios = Usuarios()
                usuario.email = body_request.email
                usuario.senha = body_request.senha
                usuario.data_cadastro = datetime.now()
                usuario.id_empresa = auth_company.id

                session.add(usuario)
                session.commit()

        except Exception as error:
            return ResponseFailure(data=str(error))

        else:
            return ResponseSuccess()

    @AutenticacaoMiddleware.apply()
    @ValidacaoCorpoRequisicaoMiddleware.apply(CadastroUsuario)
    def put(
        self,
        auth_user: Usuarios,
        auth_company: Empresas,
        body_request: CadastroUsuario,
        hash_usuario: UUID
    ) -> Response:
        try:
            with database.create_session() as session:
                usuario_localizado: Usuarios = \
                    session\
                        .query(Usuarios)\
                        .filter(
                            Usuarios.id_uuid == str(hash_usuario),
                            Usuarios.id_empresa == auth_company.id
                        )\
                        .first()

                if not usuario_localizado:
                    raise Exception('Usuario não localizado!')

                
                usuario_localizado.email = body_request.email
                usuario_localizado.senha = body_request.senha
                usuario_localizado.ativo = body_request.ativo
                usuario_localizado.data_alteracao = datetime.now()

                session.add(usuario_localizado)
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
        hash_usuario: UUID
    ) -> Response:
        try:
            with database.create_session() as session:
                usuario_localizado: Usuarios = \
                    session\
                        .query(Usuarios)\
                        .filter(
                            Usuarios.id_uuid == str(hash_usuario),
                            Usuarios.id_empresa == auth_company.id
                        )\
                        .first()

                if not usuario_localizado:
                    raise Exception('Usuario não localizado!')

                session.delete(usuario_localizado)
                session.commit()

        except Exception as error:
            return ResponseFailure(data=str(error))

        else:
            return ResponseSuccess()