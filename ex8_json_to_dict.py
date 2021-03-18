import json


def json_to_dicts(json_file):
    with open(json_file) as file:
        return json.load(file)


dictionary = json_to_dicts('example.json')
print(dictionary)