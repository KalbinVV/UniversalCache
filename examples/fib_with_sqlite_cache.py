import datetime

from UniversalCache.adapters.database_adapter import DatabaseAdapter
from UniversalCache.cache import Cache

db_cache = Cache(adapter=DatabaseAdapter(db_url='sqlite:///foo.db'))


@db_cache.cache(ttl=datetime.timedelta(seconds=60))
def fib(n: int) -> int:
    if n <= 2:
        return n

    return fib(n - 1) + fib(n - 2)


def main():
    for i in range(1, 10):
        print(fib(i), end=' ')

    print('Finished!')


if __name__ == '__main__':
    main()
