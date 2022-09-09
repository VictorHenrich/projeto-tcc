from typing import Any, Mapping
from flask import request, session
from jwt import PyJWT
from datetime import datetime

from services import server
from services.api import Middleware
from services.database import Database
from services import server
from src.utils.constantes import __NAME_SESSION_USER__, __ALGORITHMS_JWT__, __PAYLOAD_AUTHENTICATION_USER__
from src.models import Empresas, Usuarios


database: Database = server.databases.get_database()


class AutenticacaoMiddleware(Middleware):

    @staticmethod
    def __localizar_empresa(uuid_empresa: str) -> Empresas:
        with database.create_session() as session:
            empresa: Empresas = \
                session \
                    .query(Empresas) \
                    .filter(Empresas.id_uuid == uuid_empresa) \
                    .first()

            if not empresa:
                raise Exception('Empresa não localizada!')

            return empresa

    @staticmethod
    def __localizar_usuario(uuid_usuario: str, empresa: Empresas) -> Usuarios:
        with database.create_session() as session:
            usuario: Usuarios = \
                session \
                    .query(Usuarios) \
                    .filter(
                        Usuarios.id_uuid == uuid_usuario,
                        Usuarios.id_empresa == empresa.id 
                    ) \
                    .first()

            if not usuario:
                raise Exception('Usuario não localizado!')

            return usuario

    @classmethod
    def initialize(cls) -> Mapping[str, Any]:
        autenticacao: str = \
            f"{request.headers.get('Authorization') or session.get(__NAME_SESSION_USER__)}"\
                .replace('Bearer ', '')

        dados_autenticacao_jwt: Mapping[str, Any] = {
            prop: value
            for prop, value in PyJWT()\
                                    .decode(autenticacao, server.api.configs['secret_key'], __ALGORITHMS_JWT__)\
                                    .items()

            if prop in __PAYLOAD_AUTHENTICATION_USER__.keys()
        }
        
        if dados_autenticacao_jwt['expired'] <= datetime.now().timestamp():
            raise Exception('Token expirado!')

        empresa: Empresas = cls.__localizar_empresa(dados_autenticacao_jwt['uuid_company'])

        usuario: Usuarios = cls.__localizar_usuario(dados_autenticacao_jwt['uuid_user'], empresa)

        return {
            'auth_user': usuario,
            'auth_company': empresa
        }

            

            

