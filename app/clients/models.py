from app import db, ma
from marshmallow import validate, fields


# Pivot table for many to many relationship between client and studio
client_studio = db.Table('client_studio',
                         db.Column('client_id', db.Integer, db.ForeignKey('client.id'), primary_key=True),
                         db.Column('studio_id', db.Integer, db.ForeignKey('studio.id'), primary_key=True)
                         )


# Client model
class Client(db.Model):
    """
    Client model
    fields = [id, name, phone_number, password
    """
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(14), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)
    studios = db.relationship('Studio', secondary=client_studio, lazy='subquery',
                              backref=db.backref('clients', lazy=True))


class ClientSchema(ma.Schema):
    name = fields.Str(required=True)
    phone_number = fields.Str(required=True, validate=validate.Length(min=10))
    password = fields.Str(required=True, validate=validate.Length(min=6))

    class Meta:
        fields = ['id', 'name', 'phone_number', 'password']


class ClientUpdateSchema(ma.Schema):
    name = fields.Str(validate=validate.Length(min=3))
    phone_number = fields
    password = fields.Str(validate=validate.Length(min=6))

    class Meta:
        fields = ['name', 'phone_number', 'password']


class LoginOutputSchema(ma.Schema):
    token = fields.Str()
    client = fields.Nested(ClientSchema(exclude=['password']))

    class Meta:
        fields = ['token', 'client']


client_schema = ClientSchema(exclude=['password'])
clients_schema = ClientSchema(many=True, exclude=['password'])
client_input_schema = ClientSchema(exclude=['id'])
client_update_schema = ClientUpdateSchema()
client_login_output_schema = LoginOutputSchema()
client_login_input_schema = ClientSchema(exclude=['id', 'name'])
