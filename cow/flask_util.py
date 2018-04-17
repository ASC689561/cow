import json
import logging
import traceback

SUCCESS = 200  # thành công
UNKNOWN_EXCEPTION = 201  # lỗi unknown
TOKEN_INVALID = 202  # sai token


class WebServiceException:
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message


def auto_try_catch(method):
    def try_catch(*args, **kw):
        try:
            result = method(*args, **kw)
            return json.dumps({'code': SUCCESS, 'status': 'success', 'data': result, 'message': None},
                              default=lambda o: o.__dict__)
        except Exception as ex:
            logging.error(traceback.format_exc())
            code = ex.__dict__.get('code', None)
            if code is not None:
                return json.dumps({'code': code, 'status': 'error', 'data': None, 'message': str(ex)},
                                  default=lambda o: o.__dict__)
            return json.dumps({'code': UNKNOWN_EXCEPTION, 'status': 'error', 'data': None, 'message': str(ex)},
                              default=lambda o: o.__dict__)

    return try_catch
