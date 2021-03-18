import random
from measure_time import measure_time


@measure_time
def remove_duplicate_characters(input_string):
    returned_input_array = []

    for character in input_string:
        if character not in returned_input_array:
            returned_input_array.append(character)

    return ''.join(returned_input_array)


input_string = ''.join([chr(ord('a') + random.randint(0, 25)) for _ in range(10000)])
print(input_string)
print(remove_duplicate_characters(input_string))
