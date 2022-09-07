from abc import ABC, abstractmethod
from typing import Any, Mapping, Optional, Sequence


class AbstractBuilder(ABC):
    @abstractmethod
    def build(self) -> Any:
        pass


class AbstractSingleton(ABC):
    instance: Optional[Any] = None

    @classmethod
    @abstractmethod
    def get_instance(cls, *args: Sequence[str], **kwargs: Mapping[str, Any]) -> Any:
        pass