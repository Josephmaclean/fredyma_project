from app import ma
from marshmallow import fields, validate, validates, ValidationError
from app.studio import serializers as studio_serializer


class EngineerSchema(ma.Schema):
    id = fields.Integer(required=True)
    name = fields.String(validate=validate.Length(min=2))
    role = fields.String(required=True, validate=validate.OneOf([
        'mixing engineer', 'mastering engineer', 'recording engineer',
        'producer', 'song composer', 'sound engineer']))
    studio_id = fields.Integer(required=True)
    studio = fields.Nested(studio_serializer.StudioSchema(exclude=['engineers']))

    class Meta:
        fields = ['id', 'name', 'role', 'studio_id', 'studio']


create_engineer_schema = EngineerSchema(exclude=['id', 'studio', 'studio_id'])
engineer_schema = EngineerSchema()
engineers_schema = EngineerSchema(many=True)
