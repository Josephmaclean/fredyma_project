from app import db, ma
from marshmallow import  validate, fields

client_studio = db.Table('client_studio',
                         db.Column('client_id', db.Integer, db.ForeignKey('client.id'), primary_key=True),
                         db.Column('studio_id', db.Integer, db.ForeignKey('studio.id'), primary_key=True)
                         )


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(12), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    studios = db.relationship('Studio', secondary=client_studio, lazy='subquery',
                              backref=db.backref('clients', lazy=True))


class ClientSchema(ma.Schema):
    name = fields.Str(required=True)
    phone_number = fields.Str(required=True, validate=validate.Length(min=10))
    password = fields.Str(required=True, validate=validate.Length(min=6))

    class Meta:
        fields = ['id', 'name', 'phone_number', 'password']


class ClientUpdateSchema(ma.Schema):
    name = fields.Str( validate=validate.Length(min=3))
    phone_number = fields
    password = fields.Str(validate=validate.Length(min=6))

    class Meta:
        fields = ['name', 'phone_number', 'password']


client_schema = ClientSchema(exclude=['password'])
clients_schema = ClientSchema(many=True, exclude=['password'])
client_input_schema = ClientSchema()
client_update_schema = ClientUpdateSchema()