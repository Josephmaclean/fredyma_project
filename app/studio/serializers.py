from app import ma
from marshmallow import validate, fields


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
