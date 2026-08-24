from json import loads as json_loads, JSONDecodeError

def is_valid_json(json_string):
    try:
        json_loads(json_string)
        return True
    except JSONDecodeError:
        return False