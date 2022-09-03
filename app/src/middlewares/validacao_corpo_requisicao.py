from typing import Any, Mapping, Type
from flask import request

from services.api import Middleware


class ValidacaoCorpoRequisicaoMiddleware(Middleware):
    @classmethod
    def initialize(cls, class_body: Type) -> Mapping[str , Any]:
        try:
            object_body: object = class_body(**request.get_json())

        except Exception as error:
            raise Exception('Corpo da requisição não atende aos requisitos solicitados!')

        else:
            return {'body_request': object_body}

        

