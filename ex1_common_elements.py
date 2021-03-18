import random
from measure_time import measure_time


@measure_time
def common_elements(first_list, second_list):
    ret = []
    other_list = first_list
    chosen_list = second_list

    if len(first_list) < len(second_list):
        chosen_list = first_list
        other_list = second_list

    for element in chosen_list:
        if element in other_list:
            ret += [element]

    return set(ret)


@measure_time
def common_elements_v2(first_list, second_list):
    return set(first_list) & set(second_list)


inputList1 = [random.randint(1, 10) for _ in range(10000)]
inputList2 = [random.randint(1, 10) for _ in range(10000)]
print(common_elements(inputList1, inputList2))
print(common_elements_v2(inputList1, inputList2))
