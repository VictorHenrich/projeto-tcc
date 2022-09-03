from typing import Any, Mapping, Callable, Sequence
from uuid import UUID, uuid1, uuid3, uuid4, uuid5


def create_uuid(version: int = 4, *args: Sequence[Any], **kwargs: Mapping[str, Any] ) -> str:
    versions_uuid: Mapping[int, Callable] = {
        1: uuid1,
        3: uuid3,
        4: uuid4,
        5: uuid5
    }

    return str(versions_uuid[version](*args, **kwargs))