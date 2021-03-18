def cache(func):
    function_to_result = dict()

    def inner(*args, **kwargs):
        if func.__name__ in function_to_result:
            print("Used cached value!")
            return function_to_result[func.__name__]

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
print(func2())
print(func1())
