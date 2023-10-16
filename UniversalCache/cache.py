from functools import wraps
from typing import Callable

from UniversalCache.abstract_adapter import AbstractAdapter


class Cache:
    def __init__(self, adapter: AbstractAdapter):
        self.__adapter = adapter

    def cache(self, **params):
        def _decorate(function: Callable):
            @wraps(function)
            def wrapper(*args, **kwargs):
                if self.__adapter.contains(function, params, *args, **kwargs):
                    return self.__adapter.get(function, params, *args, **kwargs)

                value = function(*args, **kwargs)

                self.__adapter.set(function, value, params, *args, **kwargs)

                return value

            return wrapper

        return _decorate
