import os, json, jwt, bcrypt, datetime
from dotenv import load_dotenv
from app import dotenv_path
from flask import Blueprint, request, Response, abort
from sqlalchemy.exc import SQLAlchemyError

load_dotenv(dotenv_path)

from app import db
from .models import (Studio, studio_input_schema,
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
        abort(Response(json.dumps(errors), 400, mimetype='application/json'))
    studio_instance = Studio.query.filter_by(email=email).first()

    if bcrypt.checkpw(password.encode('utf-8'), studio_instance.password.encode('utf-8')):
        secret = os.getenv('SECRET_KEY')
        token = jwt.encode({'id': studio_instance.id}, secret, algorithm='HS256')
        result = {
            'token': token,
            'studio': studio_instance
        }
        return Response(studio_signin_schema.dumps(result), 200, mimetype='application/json')


@studio.route('/studio/<int:studio_id>', methods=['GET'])
def get_studio(studio_id):
    try:
        studio = Studio.query.filter_by(id=studio_id).first_or_404()
        result = studio_schema.dumps(studio)
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