import time

def measure_time(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print(f'Function {func.__name__} took: {time.time() - start_time} seconds')
        return result

    return inner