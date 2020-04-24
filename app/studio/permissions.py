import os, jwt, datetime, inspect, json
from flask import Response,abort, request
from functools import wraps
from app import dotenv_path
from dotenv import load_dotenv

load_dotenv(dotenv_path)


def studio_login_required(func):
    """
        a wrapper around views to authorize requests
    :param func:
    :return: function
    """
    wraps(func)

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
            return abort(Response(json.dump(message), 401, mimetype='application/json'))

        # check if payload ia an argument of function
        # if is argument return user_id
        if 'user_id' in inspect.getfullargspec(func).args:
            kwargs['user_id'] = payload['studio_id']
    return view_wrapper()