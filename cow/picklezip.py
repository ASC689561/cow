import gzip
import io
import pickle


def zip_obj(obj, file_name=None):
    with io.BytesIO() as zip_buffer:
        f = gzip.open(zip_buffer, 'wb')
        pickle.dump(obj, f)

        if not file_name:
            with open(file_name, 'wb') as out:
                out.write(zip_buffer.read())
        zip_buffer.seek(0)
        return zip_buffer.read()


def unzip_obj(file_name):
    f = gzip.open(file_name, 'rb')
    obj = pickle.load(f)
    f.close()
    return obj
