import datetime

from UniversalCache.adapters.dict_adapter import DictAdapter
from UniversalCache.cache import Cache

dict_cache = Cache(adapter=DictAdapter())


@dict_cache.cache(ttl=datetime.timedelta(seconds=60))
def fib(n: int) -> int:
    if n <= 2:
        return n

    return fib(n - 1) + fib(n - 2)


def main():
    for i in range(1, 100):
        print(fib(i), end='')

    print('Finished!')


if __name__ == '__main__':
    main()
