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
    activation_code = db.Column(db.Integer)
    studios = db.relationship('Studio', secondary=client_studio, lazy='subquery',
                              backref=db.backref('clients', lazy=True))


