import abc
from typing import Any, Callable


class AbstractAdapter(abc.ABC):
    @abc.abstractmethod
    def get(self, function, params: dict, *args, **kwargs) -> Any:
        ...

    @abc.abstractmethod
    def set(self, function, params: dict, value: Any, *args, **kwargs) -> None:
        ...

    @abc.abstractmethod
    def contains(self, function, params: dict, *args, **kwargs) -> bool:
        ...
