from app import ma
from marshmallow import validate, fields


class EngineerSchema(ma.Schema):
    id = fields.Integer(required=True)
    name = fields.String(validate=validate.Length(min=2))
    role = fields.String(required=True, validate=validate.OneOf([
        'mixing engineer', 'mastering engineer', 'recording engineer',
        'producer', 'song composer', 'sound engineer']))

    class Meta:
        fields = ['id', 'name', 'role']


class StudioSchema(ma.Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True, error="not a valid email")
    password = fields.Str(required=True, validate=validate.Length(min=6))
    engineers = fields.Nested(EngineerSchema(many=True))

    class Meta:
        fields = ['id', 'name', 'email', 'password', 'engineers']


class LoginSchema(ma.Schema):
    token = fields.Str()
    studio = fields.Nested(StudioSchema(exclude=['password']))

    class Meta:
        fields = ['token', 'studio']


studio_schema = StudioSchema(exclude=['password'])
studio_input_schema = StudioSchema()
studios_schema = StudioSchema(many=True, exclude=['password', 'engineers'])
studio_schema_signin_input = StudioSchema(exclude=['name', 'engineers'])
studio_signin_schema = LoginSchema()
