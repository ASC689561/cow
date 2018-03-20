import gzip
import pickle
import tempfile


def zip_obj(obj, file_name=None):
    if file_name is None:
        file_name = tempfile.mktemp()

    with gzip.open(file_name, 'wb') as f:
        pickle.dump(obj, f)

    with gzip.open(file_name, 'rb') as f:
        data = f.read()
        return data


def unzip_obj(file_name):
    f = gzip.open(file_name, 'rb')
    obj = pickle.load(f)
    f.close()
    return obj
