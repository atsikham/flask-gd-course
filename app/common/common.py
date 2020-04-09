import functools
import jwt
import json

from flask import request, Response
from flask import current_app as app
from sqlalchemy.exc import StatementError


def token_required(f):
    """
    Legacy function to support jwt
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return Response("{'error': 'Need a valid token to display this page'}", 401, mimetype='application/json')

    return wrapper


def error_handler(f):
    """
    Handler to process exceptions for routes
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            response = f(*args, **kwargs)
        except StatementError as e:
            invalid_msg = {
                'error': 'Unsupported field type'
            }
            response = Response(json.dumps(invalid_msg), status=400, mimetype='application/json')
        except Exception as e:
            invalid_msg = {
                'error': str(e)
            }
            response = Response(json.dumps(invalid_msg), status=400, mimetype='application/json')
        finally:
            return response

    return wrapper
