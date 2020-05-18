# from app import ma
from marshmallow import fields, validate, Schema
from ..studio import serializers as studio_serializer


class EngineerSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True, validate=validate.Length(min=2))
    role = fields.String(required=True, validate=validate.OneOf([
        'mixing engineer', 'mastering engineer', 'recording engineer',
        'producer', 'song composer', 'sound engineer']))
    studio_id = fields.Integer(required=True)
    studio = fields.Nested(studio_serializer.StudioSchema(exclude=['engineers']))

    class Meta:
        fields = ['id', 'name', 'role', 'studio_id', 'studio']


class UpdateEngineerSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=2))
    role = fields.String(required=True, validate=validate.OneOf([
        'mixing engineer', 'mastering engineer', 'recording engineer',
        'producer', 'song composer', 'sound engineer']))

    class Meta:
        fields = ['name', 'role']


create_engineer_schema = EngineerSchema(exclude=['id', 'studio', 'studio_id'])
engineer_schema = EngineerSchema()
update_engineer_schema = UpdateEngineerSchema()
