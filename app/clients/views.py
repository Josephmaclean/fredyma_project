import bcrypt, json
from flask import Blueprint, request, Response, abort
from dotenv import load_dotenv
from app import db, dotenv_path
from sqlalchemy.exc import SQLAlchemyError

load_dotenv(dotenv_path)

from .models import (Client, client_input_schema,
                     client_schema, clients_schema, client_update_schema)

clients = Blueprint('clients', __name__)


@clients.route('/clients', methods=['POST'])
def create_client():
    errors = client_input_schema.validate(request.json)

    if errors:
        abort(Response(json.dumps(errors), 400, mimetype='application/json'))

    client_details = request.json
    name = client_details['name']
    phone_number = client_details['phone_number']
    password = client_details['password']

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    try:
        new_client = Client(name=name, phone_number=phone_number, password=hashed_password)
        db.session.add(new_client)
        db.session.commit()
        result = client_schema.dumps(new_client)
        return Response(result, 201, mimetype='application/json')
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error


@clients.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    try:
        client = Client.query.filter_by(id=client_id).first_or_404()
        result = client_schema.dumps(client)
        return Response(result, 200, mimetype='application/json')
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error


@clients.route('/clients/<int:client_id>', methods=['PATCH'])
def edit_client(client_id):
    errors = client_update_schema.validate(request.json)
    if errors:
        abort(Response(json.dumps(errors), 400, mimetype='application/json'))

    try:
        client_details = request.json
        client = Client.query.filter_by(id=client_id)
        client.update(dict(client_details))
        db.session.commit()
        return Response(client_schema.dumps(client), 200, mimetype='application/json')
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
