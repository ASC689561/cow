import logging
import traceback
from functools import wraps

SUCCESS = 200  # thành công
UNKNOWN_EXCEPTION = 201  # lỗi unknown
AUTHEN_FAILED = 202  # sai token


class WebServiceException(RuntimeError):
    def __init__(self, code: int, message: str):
        super(WebServiceException, self).__init__(message)
        self.code = code
        self.message = message


class AuthenFailedException(WebServiceException):
    def __init__(self):
        super(AuthenFailedException, self).__init__(AUTHEN_FAILED, 'Authentication failed')


def check_auth(check_function):
    def check_token_method(method):
        @wraps(method)
        def check(*args, **kw):
            if not check_function():
                raise AuthenFailedException()
            result = method(*args, **kw)
            return result

        return check

    return check_token_method


def auto_try_catch(method):
    @wraps(method)
    def try_catch(*args, **kw):
        from flask import jsonify

        try:
            result = method(*args, **kw)
            return jsonify({'code': SUCCESS, 'status': 'success', 'data': result, 'message': None}), 200, {
                'ContentType': 'application/json'}
        except Exception as ex:
            logging.error(traceback.format_exc())
            code = ex.__dict__.get('code', None)
            if code is not None:
                return jsonify({'code': code, 'status': 'error', 'data': None, 'message': str(ex)}), code, {'ContentType': 'application/json'}
            return jsonify({'code': UNKNOWN_EXCEPTION, 'status': 'error', 'data': None, 'message': str(ex)}), 500, {'ContentType': 'application/json'}

    return try_catch
