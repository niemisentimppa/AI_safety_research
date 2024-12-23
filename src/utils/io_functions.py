import json

# Write data to a given json file path
def writeJSON(json_path, json_data):
    if not isinstance(json_path, str):
        raise TypeError("json_path must be a string")
    with open(json_path, 'w', encoding='utf-8') as f:
        # use parameters sort_keys='true' or default='str' if you must
        json.dump(json_data, f, ensure_ascii=False, indent=4)

# Give json file path as parameter, get your data from json file back
def readJSON(json_path):
    if not isinstance(json_path, str):
        raise TypeError("json_path must be a string")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


