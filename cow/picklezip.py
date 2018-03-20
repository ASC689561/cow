import gzip
import io
import pickle
import tempfile

import os


def zip_obj(obj, file_name=None):
    if file_name is None:
        tem_file = tempfile.mktemp()

    with gzip.open(tem_file, 'wb') as f:
        pickle.dump(obj, f)

    with gzip.open(tem_file, 'rb') as f:
        data = f.read()
        return data


def unzip_obj(file_name):
    f = gzip.open(file_name, 'rb')
    obj = pickle.load(f)
    f.close()
    return obj
