from flask import Response
from typing import Any, Callable, Optional, Sequence, Mapping
from .utils.responses import ResponseFailure


class Middleware:
    @classmethod
    def initialize(cls, *args: Sequence[Any], **kwargs: Mapping[str, Any]) -> Optional[Mapping[str, Any]]:
        raise NotImplementedError('Method "initialize" the middleware not implemented!')

    @classmethod
    def redirect(cls, error: Exception) -> Response:
        return ResponseFailure(data=str(error))

    @classmethod
    def apply(cls, *args: Sequence[Any], **kwargs: Mapping[str, Any]) -> Callable:
        def wrapper(function: Callable) -> Any:
            def w(*a: Sequence[Any], **k: Mapping[str, Any]) -> Any:
                try:
                    params_initialize: Optional[Mapping[str, Any]] = cls.initialize(*args, **kwargs)

                except Exception as error:
                    return cls.redirect(error)

                else:
                    return function(*a, **{**k, **(params_initialize or dict())})

            return w

        return wrapper