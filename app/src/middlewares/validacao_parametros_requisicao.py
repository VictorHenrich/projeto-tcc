from typing import Any, Mapping, Type
from flask import request

from services.api import Middleware


class ValidacaoParametrosRequisicaoMiddleware(Middleware):
    @classmethod
    def initialize(cls, class_params: Type) -> Mapping[str, Any]:
        try:
            object_params: object = class_params(**request.args)

        except Exception as error:
            raise Exception('Parametros da requisição não atende aos requisitos solicitados!')

        else:
            return {'params_request': object_params}