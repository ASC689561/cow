import logging


def execute_curl(curl, json_out=True):
    import json
    import subprocess
    out = ''
    try:
        p = subprocess.Popen(curl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if json_out:
            return json.loads(out.decode())
        else:
            return out
    except Exception as e:
        logging.error('Error when execute curl[{}], resull[{}]'.format(curl, out))
        raise e
