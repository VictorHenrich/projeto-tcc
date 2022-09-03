from flask_restful import Resource
from flask import Response
from typing import Sequence, Mapping, Any

from .utils.responses import ResponseNotFound


class Controller(Resource):
    def get(self, *args: Sequence[Any], **kwargs: Mapping[str, Any]) -> Response:
        return ResponseNotFound()

    def post(self, *args: Sequence[Any], **kwargs: Mapping[str, Any]) -> Response:
        return ResponseNotFound()

    def put(self, *args: Sequence[Any], **kwargs: Mapping[str, Any]) -> Response:
        return ResponseNotFound()

    def delete(self, *args: Sequence[Any], **kwargs: Mapping[str, Any]) -> Response:
        return ResponseNotFound()

    def patch(self, *args: Sequence[Any], **kwargs: Mapping[str, Any]) -> Response:
        return ResponseNotFound()