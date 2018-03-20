import gzip
import io
import pickle


def zip_obj(obj, file_name=None):
    zip_buffer = io.BytesIO()
    f = gzip.open(zip_buffer, 'wb')
    pickle.dump(obj, f)

    if not file_name:
        with open(file_name, 'wb') as out:
            out.write(zip_buffer.read())


def unzip_obj(file_name):
    f = gzip.open(file_name, 'rb')
    obj = pickle.load(f)
    f.close()
    return obj
