import datetime
from typing import Callable, Any

from UniversalCache.abstract_adapter import AbstractAdapter
from UniversalCache.adapters.cache_ttl_value_pair import CacheTTLValuePair


class DictAdapter(AbstractAdapter):
    def __init__(self):
        self.__dict: dict[str, CacheTTLValuePair] = dict()

    @classmethod
    def __make_key(cls, function, *args, **kwargs) -> str:
        return f'{function.__name__}:{function.__module__}:{str(args)}{str(kwargs)}'

    def get(self, function, params: dict, *args, **kwargs) -> Any:
        key = self.__make_key(function, *args, **kwargs)

        return self.__dict[key].value

    def set(self, function, value: Any, params: dict, *args, **kwargs) -> None:
        ttl = params['ttl'] if 'ttl' in params else None

        key = self.__make_key(function, *args, **kwargs)

        key_value_pair = CacheTTLValuePair(
            expire_time=datetime.datetime.now() + ttl if ttl is not None else None,
            value=value
        )

        self.__dict[key] = key_value_pair

    def contains(self, function, params: dict, *args, **kwargs) -> bool:
        key = self.__make_key(function, *args, **kwargs)

        if key not in self.__dict:
            return False

        key_value_pair = self.__dict[key]

        if key_value_pair.expire_time is None:
            return key_value_pair.value

        if datetime.datetime.now() > key_value_pair.expire_time:
            return False
        else:
            return True
