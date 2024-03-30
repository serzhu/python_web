from time import time
#from functools import wraps

def async_timed():
    def wrapper(func):
        async def wrapped(*args, **kwargs):
            print(f'Strat function {func.__name__} with {args} {kwargs}')
            start_time = time()
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                print(f'End function {func.__name__} in {round((time() - start_time),2)}')
        return wrapped
    return wrapper
            