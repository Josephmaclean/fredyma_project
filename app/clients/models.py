from app import db
import json


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(12), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)

    def __repr__(self):
        client_object = {
            'name': self.name,
            'phone_number': self.phone_number,
        }
        return json.dumps(client_object)
