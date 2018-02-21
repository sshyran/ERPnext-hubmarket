import json

def safe_json_loads(string):
    try:
        string = json.loads(string)
    except Exception as e:
        pass

    return string

def assign_if_empty(a, b):
    return a if a else b