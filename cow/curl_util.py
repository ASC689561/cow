import logging


class CurlNotFound(Exception):
    def __init__(self):
        super(CurlNotFound, self).__init__('Curl not found in')


def execute_curl(curl, json_out=True):
    import json
    import subprocess
    out = ''
    try:
        p = subprocess.Popen(curl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode == 127:
            raise CurlNotFound()
        if json_out:
            return json.loads(out.decode())
        else:
            return out
    except Exception as e:
        logging.error('Error when execute curl[{}], result[{}] error[{}]'.format(curl, out, err))
        raise e
