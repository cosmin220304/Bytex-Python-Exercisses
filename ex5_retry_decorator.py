import random


def retry(func):
    def inner(*args, **kwargs):
        while not func():
            print("Retrying...")

    return inner


@retry
def get_random_bool():
    return random.randint(0, 100) < 50


get_random_bool()
