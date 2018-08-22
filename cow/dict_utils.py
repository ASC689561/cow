def md5(dic:dict)->str:
    import hashlib
    import json

    data_md5 = hashlib.md5(json.dumps(dic, sort_keys=True).encode()).hexdigest()
    return str(data_md5)


def remove_key_except(dic, keys):
    remove_keys = []
    for v in dic:
        if v not in keys:
            remove_keys.append(v)
    for v in remove_keys:
        dic.pop(v)
