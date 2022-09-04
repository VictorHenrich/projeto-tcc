from dataclasses import dataclass
from typing import Any, Mapping
from jwt import PyJWT
from datetime import datetime, timedelta
from flask import session

from services import server
from services.database import Database
from services.api import Controller
from src.middlewares import ValidacaoParametrosRequisicaoMiddleware
from src.models import Empresas, Usuarios
from src.utils.constantes import (
    __PAYLOAD_AUTHENTICATION_USER__, 
    __ALGORITHMS_JWT__, 
    __NAME_SESSION_USER__
)
from services.api.utils.responses import (
    Response, 
    ResponseFailure, 
    ResponseSuccess
)


database: Database = server.databases.get_database()


@dataclass
class ParametrosAutenticacao:
    hash_user: str
    hash_company: str


class AutenticacaoController(Controller):

    def __localizar_empresa(self, hash_empresa: str) -> Empresas:
        with database.create_session() as session:
            empresa: Empresas = \
                session\
                    .query()\
                    .filter(Empresas.id_uuid == hash_empresa)\
                    .first()

            if not empresa:
                raise Exception('Empresa não localizada!')

            return empresa            

    def __localizar_usuario(self, hash_usuario: str, dados_empresa: Empresas) -> Usuarios:
        with database.create_session() as session:
            usuario: Usuarios = \
                session\
                    .query(Usuarios)\
                    .filter(
                        Usuarios.id_uuid == hash_usuario,
                        Usuarios.id_empresa == dados_empresa.id
                    )\
                    .first()

            if not usuario:
                raise Exception('Usuario não localizado!')

    @ValidacaoParametrosRequisicaoMiddleware.apply(ParametrosAutenticacao)
    def get(self, params_request: ParametrosAutenticacao) -> Response:
        try:
            dados_empresa: Empresas = self.__localizar_empresa(params_request.hash_company)
            dados_usuario: Usuarios = self.__localizar_usuario(params_request.hash_user, dados_empresa)
            
            dados_autenticacao: Mapping[str, Any] = {**__PAYLOAD_AUTHENTICATION_USER__}

            dados_autenticacao['uuid_company'] = dados_empresa.id_uuid
            dados_autenticacao['uuid_user'] = dados_usuario.id_uuid
            dados_autenticacao['expired'] = (datetime.now() + timedelta(minutes=5)).timestamp()

            token: str = \
                f"Bearer {PyJWT().encode(dados_autenticacao, algorithm=list(__ALGORITHMS_JWT__)[0])}"


            session[__NAME_SESSION_USER__] = token

        except Exception as error:
            return ResponseFailure(data=str(error))

        else:
            resposta: Mapping[str, str] = {
                'token': token,
                'token_type': 'Bearer'
            }

            return ResponseSuccess(data=resposta)