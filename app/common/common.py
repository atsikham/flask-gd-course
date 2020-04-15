import functools
import json

from flask import Response
from sqlalchemy.exc import StatementError
from app import file_logger


def error_handler(f):
    """
    Handler to process exceptions for routes
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            response = f(*args, **kwargs)
        except StatementError:
            invalid_msg = {
                'error': 'Unsupported field or field type'
            }
            response = Response(json.dumps(invalid_msg), status=400, mimetype='application/json')
        except Exception as e:
            file_logger.exception('Exception occurred. See information below')
            invalid_msg = {
                'error': str(e)
            }
            response = Response(json.dumps(invalid_msg), status=400, mimetype='application/json')
        finally:
            return response

    return wrapper
