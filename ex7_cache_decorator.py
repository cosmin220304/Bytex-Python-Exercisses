from datetime import timedelta, datetime
import time

expiry_time = timedelta(seconds=5)


def cache(func):
    function_to_result = dict()
    cache_expiration = dict(date=datetime.now())

    def inner(*args, **kwargs):
        if func.__name__ in function_to_result:
            if cache_expiration['date'] >= datetime.now():
                print('Used cached value!')
                return function_to_result[func.__name__]
            else:
                print('Cached expired!')
                cache_expiration['date'] = datetime.now() + expiry_time

        result = func(*args, **kwargs)
        function_to_result[func.__name__] = result
        return result

    return inner


@cache
def func1():
    return 1


@cache
def func2():
    return 2


print(func1())
print(func1())
time.sleep(5)
print(func1())
print(func1())
print(func2())
print(func1())
print(func1())
