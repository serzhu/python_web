
import redis
from redis_lru import RedisLRU
import timeit

client = redis.StrictRedis(host="localhost", port=6379, password=None)
my_cache = RedisLRU(client)


def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


@my_cache
def fibonacci_cache(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_cache(n - 1) + fibonacci_cache(n - 2)


if __name__ == '__main__':

    start_time = timeit.default_timer()
    fibonacci(38)
    print(f'Duration: {timeit.default_timer() - start_time}')

    start_time = timeit.default_timer()
    fibonacci_cache(38)
    print(f'Duration: {timeit.default_timer() - start_time}')
