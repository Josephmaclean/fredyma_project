import jwt, os, datetime, inspect, json
from functools import wraps
from flask import g, request, redirect, Response, abort
from dotenv import load_dotenv
from app import dotenv_path
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

# load .env variables
load_dotenv(dotenv_path)


def client_login_required(func):
    """
    a wrapper around views to authorize requests
    :param func:
    :return: function
    """

    @wraps(func)
    def view_wrapper(*args, **kwargs):
        authorization = ""
        try:
            authorization = request.headers['Authorization']
        except KeyError:
            abort(Response("unauthorized", 401, mimetype='application/json'))
        token = authorization.split()[1]
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            if 'is_client' in payload and payload['is_client'] is True:
                if 'user_id' in inspect.getfullargspec(func).args:
                    kwargs['user_id'] = payload['id']
                return func(*args, **kwargs)
            else:
                abort(Response("unauthorized", 401, mimetype='application/json'))
        except ExpiredSignatureError:
            message = {
                'error': 'token expired'
            }
            return abort(Response(json.dumps(message), 401, mimetype='application/json'))
        except InvalidSignatureError:
            message = {
                'error': 'invalid token'
            }
            return abort(Response(json.dumps(message), 401, mimetype='application/json'))

    return view_wrapper
