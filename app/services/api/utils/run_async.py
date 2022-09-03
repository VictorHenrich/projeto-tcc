import asyncio
from typing import Any, Callable, Sequence, Mapping


class RunAsync:
    @staticmethod
    def run(function: Callable) -> Callable:
        def wrapper(*args: Sequence[Any], **kwargs: Mapping[str, Any]):
            return asyncio.run(function(*args, **kwargs))

        return wrapper
