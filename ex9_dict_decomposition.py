def recursive_decomposition(prev_string, dictionary_input):
    for (key, val) in dictionary_input.items():
        if type(val) is dict:
            recursive_decomposition(f'{prev_string}.{key}', val)
        else:
            print(f'{prev_string}.{key}.{val}')


def dict_decomposition(dictionary_input):
    for (key, val) in dictionary_input.items():
        if type(val) is dict:
            recursive_decomposition(key, val)
        else:
            print(f'{key}.{val}')


my_dict = {
    'a': 1,
    'b': {'c': 2},
    'd': {
        'e': {'f': 3},
        'g': 4,
        'test': {
            "test2": 3,
            "test3": 4
        }
    }
}
dict_decomposition(my_dict)
