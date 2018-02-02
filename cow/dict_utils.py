def get_md5(dic):
    import hashlib
    import json

    data_md5 = hashlib.md5(json.dumps(dic, sort_keys=True).encode()).hexdigest()
    return str(data_md5)
