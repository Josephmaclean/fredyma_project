from app import ma
from marshmallow import validate, fields


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


class ClientActivationSanitizer(ma.Schema):
    client_id = fields.Integer(required=True)
    activation_code = fields.Integer(required=True)

    class Meta:
        fields = ['client_id', 'activation_code']


client_schema = ClientSchema(exclude=['password'])
clients_schema = ClientSchema(many=True, exclude=['password'])
client_input_schema = ClientSchema(exclude=['id'])
client_update_schema = ClientUpdateSchema()
client_login_output_schema = LoginOutputSchema()
client_login_input_schema = ClientSchema(exclude=['id', 'name'])
client_activation_sanitizer = ClientActivationSanitizer()
