import json
import os

def getInputs():
    data = {};
    with open(os.path.join('inputs', 'input.json'), 'r') as json_file:
        data = json.load(json_file)
        # print(data);
    return data;