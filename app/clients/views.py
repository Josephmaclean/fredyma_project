from flask import  Blueprint, request
from .models import Client, db

clients = Blueprint('clients', __name__)


@clients.route('/clients', methods = ['POST'])
def create_client():
    client_details = request.get_json()
    name = client_details['name']
    phone_number = client_details['phone_number']
    password = client_details['password']

    new_client = Client(name=name, phone_number=phone_number, password=password)
    db.session.add(new_client)
    db.session.commit()
    return client_details
