from app import db, ma
from marshmallow import validate, fields


class Studio(db.Model):
    __tablename__ = 'studio'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)


class StudioSchema(ma.Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True, error="not a valid email")
    password = fields.Str(required=True, validate=validate.Length(min=6))

    class Meta:
        fields = ['id', 'name', 'email', 'password']


class LoginSchema(ma.Schema):
    token = fields.Str()
    studio = fields.Nested(StudioSchema(exclude=['password']))

    class Meta:
        fields = ['token', 'studio']


studio_schema = StudioSchema(exclude=['password'])
studio_input_schema = StudioSchema()
studios_schema = StudioSchema(many=True, exclude=['password'])
studio_schema_signin_input = StudioSchema(exclude=['name'])
studio_signin_schema = LoginSchema()
