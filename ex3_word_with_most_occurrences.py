import random
import re
from measure_time import measure_time


@measure_time
def word_with_most_occurrences(input_string):
    sentences = re.split("\s+|,|/.|/?|!", input_string)
    maxx = 0
    returned_word = ''
    word_count = dict()

    for word in sentences:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

        if word_count[word] > maxx:
            maxx = word_count[word]
            returned_word = word

    return returned_word


def generate_input():
    generated = []
    for _ in range(10000):
        random_int = random.randint(0, 26)
        if random_int == 26:
            generated.append(" ")
        else:
            generated.append(chr(ord("a") + random_int))
    return ''.join(generated)


input_string = generate_input()
print(input_string)
print(word_with_most_occurrences(input_string))
