def get_md5(dic):
    import hashlib
    import json

    data_md5 = hashlib.md5(json.dumps(dic, sort_keys=True).encode()).hexdigest()
    return str(data_md5)


def update(dic1, dic2):
    for v in dic1.keys():
        if v in dic2:
            dic1[v] = dic2[v]


def remove_key_except(dic, keys):
    remove_keys=[]
    for v in dic:
        if v not in keys:
            remove_keys.append(v)
    for v in remove_keys:
        dic.pop(v)

