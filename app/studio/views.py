import bcrypt
import datetime
import json
import jwt
import os

from dotenv import load_dotenv
from flask import Blueprint, request, Response, abort
from sqlalchemy.exc import SQLAlchemyError

from app import dotenv_path

load_dotenv(dotenv_path)

from app import db
from .models import Studio
from .serializers import (studio_input_schema,
                          studio_schema, studio_schema_signin_input,
                          studio_signin_schema, studios_schema)

studio = Blueprint('studio', __name__)


@studio.route('/studio', methods=['POST'])
def create_studio():
    errors = studio_input_schema.validate(request.json)
    details = request.json
    name = details["name"]
    email = details["email"]
    password = details["password"]

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    # decode utf-8 encoded password  before storing in DB
    decoded_hashed_password = hashed_password.decode('utf-8')

    if errors:
        abort(Response(json.dumps(errors), 400, mimetype='application/json'))

    try:
        new_studio = Studio(name=name, email=email, password=decoded_hashed_password)
        db.session.add(new_studio)
        db.session.commit()
        result = studio_schema.dumps(new_studio)
        return Response(result, 201, mimetype='application/json')
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error


@studio.route('/auth/studio', methods=['POST'])
def signin():
    details = request.json
    errors = studio_schema_signin_input.validate(details)
    email = details['email']
    password = details['password']

    if errors:
        return abort(Response(json.dumps(errors), 400, mimetype='application/json'))
    studio_instance = Studio.query.filter_by(email=email).first()
    if studio_instance is None:
        message = {
            'error': 'unauthorized'
        }
        return abort(Response(json.dumps(message), 401, mimetype='application/json'))

    if bcrypt.checkpw(password.encode('utf-8'), studio_instance.password.encode('utf-8')):
        secret = os.getenv('SECRET_KEY')
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(days=5)
        token = jwt.encode({'id': studio_instance.id, 'exp': expiration_date, 'is_studio': True},
                           secret, algorithm='HS256')
        result = {
            'token': token,
            'studio': studio_instance
        }
        return Response(studio_signin_schema.dumps(result), 200, mimetype='application/json')


@studio.route('/studio/<int:studio_id>', methods=['GET'])
def get_studio(studio_id):
    try:
        studio_query = Studio.query.get(studio_id)
        result = studio_schema.dumps(studio_query)
        return Response(result, 200, mimetype='application/json')
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error


@studio.route('/studio', methods=['GET'])
def get_all_studios():
    try:
        studios = Studio.query.all()
        result = studios_schema.dumps(studios)
        return Response(result, 200, mimetype='application/json')
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error


@studio.route('/studio/<int:studio_id>', methods=['DELETE'])
def delete_studio(studio_id):
    Studio.query.filter_by(id=studio_id).delete()
    db.session.commit()
    return Response("", 204, mimetype='application/json')


# TODO: update studio
