def count_calls(func):
    function_to_number = dict()

    def inner(*args, **kwargs):
        if func.__name__ in function_to_number:
            function_to_number[func.__name__] += 1
        else:
            function_to_number[func.__name__] = 1

        print(f"{func.__name__} was called {function_to_number[func.__name__]} times!")

        result = func(*args, **kwargs)
        return result

    return inner


@count_calls
def func1():
    pass


@count_calls
def func2():
    pass


func1()
func2()
func1()