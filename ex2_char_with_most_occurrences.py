import random
from measure_time import measure_time


@measure_time
def char_with_most_occurrences(input_string):
    maxx = 0
    returned_character = ''
    char_count = dict()

    for character in input_string:
        if character in char_count:
            char_count[character] += 1
        else:
            char_count[character] = 1

        if char_count[character] > maxx:
            maxx = char_count[character]
            returned_character = character

    return returned_character


input_string = ''.join([chr(ord('a') + random.randint(0, 25)) for _ in range(10000)])
print(input_string)
print(char_with_most_occurrences(input_string))
