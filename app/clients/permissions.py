import jwt, os, datetime, inspect, json
from functools import wraps
from flask import g, request, redirect, Response, abort
from dotenv import load_dotenv
from app import dotenv_path

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
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])

        if payload['exp'] < datetime.datetime.utcnow():
            message = {
                'error': 'token expired'
            }
            return abort(Response(json.dumps(message), 401, mimetype='application/json'))
        # check if payload ia an argument of function
        # if is argument return user_id
        if 'payload' in inspect.getfullargspec(func).args:
            kwargs['payload'] = payload

        return func(*args, **kwargs)

    return view_wrapper