import json


def read_abi():
    json_file_path = '<paste Election.json path here>'

    with open(json_file_path, 'r') as file:
        data = json.load(file)
        return data['abi']


