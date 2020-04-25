import bcrypt, json, jwt, os, datetime
from flask import Blueprint, request, Response, abort, current_app
from dotenv import load_dotenv
from app import db, dotenv_path
from sqlalchemy.exc import SQLAlchemyError
from app.utils import sms
from blinker import Namespace

# Signal for events
client_events = Namespace()
client_signal = client_events.signal('client_signal')

load_dotenv(dotenv_path)

from .models import (Client, client_input_schema,
                     client_schema, clients_schema, client_update_schema,
                     client_login_output_schema, client_login_input_schema)

from .permissions import client_login_required

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
        new_client = Client(name=name, phone_number=phone_number,
                            password=hashed_password, active=False)
        db.session.add(new_client)
        db.session.commit()
        # emit send sms signal
        client_signal.send(current_app._get_current_object(), event_id=1,
                           phone_number=phone_number)

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
@client_login_required
def edit_client(client_id):
    # print()
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


@clients.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    client = Client.query.filter_by(id=client_id)
    client.delete()
    db.session.commit()
    return Response("", 204, mimetype='application/json')


@clients.route('/auth/studio', methods=['POST'])
def signin():
    errors = client_login_input_schema.validate(request.json)
    if errors:
        abort(Response(json.dumps(errors), 400, mimetype='application/json'))
    details = request.json
    phone_number = details['phone_number']
    password = details['password']

    client = Client.query.filter_by(phone_number=phone_number).first()
    if client == {}:
        message = {
            'error': 'unauthorized'
        }
        abort(Response(json.dumps(message), 401, mimetype='application/json'))

    instance_id = client.id
    if bcrypt.checkpw(password.encode('utf-8'), client.password.encode('utf-8')):
        secret = os.getenv('SECRET_KEY')
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(days=5)
        token = jwt.encode({'id': instance_id, 'exp': expiration_date, 'is_client': True},
                           secret, algorithm='HS256')
        result = {
            'token': token,
            'client': client
        }
        data = client_login_output_schema.dumps(result)
        return Response(data, 200, mimetype='application/json')


@client_signal.connect
def send_sms(app, **kwargs):
    # send SMS
    message = 'account created successfully',
    sender = '+441158245751'
    receiver = kwargs['phone_number']
    sms.send_sms(body=message, sender=sender, receiver=receiver)