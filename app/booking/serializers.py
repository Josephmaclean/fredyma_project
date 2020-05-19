import datetime
from app import ma
from marshmallow import fields, validate, validates
from marshmallow.exceptions import ValidationError
from ..engineers import serializers as engineer_serializer
from ..studio import serializers as studio_serializer
from ..clients import serializers as client_serializer


class BookingSchema(ma.Schema):
    studio_id = fields.Integer()
    client_id = fields.Integer()
    start_time = fields.DateTime()
    end_time = fields.DateTime()
    status = fields.Boolean()

    class Meta:
        fields = ['id', 'studio_id', 'client_id', 'start_time', 'end_time', 'status', ]


class BookingInputSchema(ma.Schema):
    studio_id = fields.Integer(required=True)
    engineer_id = fields.Integer(required=True)
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)
    date = fields.Date(required=True)
    session_type = fields.String(required=True, validate=validate.Length(min=5))

    @validates('date')
    def validate_date(self, value):
        now = datetime.datetime.utcnow().date()
        if now > value:
            raise ValidationError('invalid date')

    class Meta:
        fields = ['studio_id', 'start_time', 'end_time',
                  'date', 'session_type']


class BookingViewSchema(ma.Schema):
    start_time = fields.Time()
    end_time = fields.Time()
    studio = fields.Nested(studio_serializer.StudioSchema(exclude=['engineers', 'password', 'email']))
    sound_engineer = fields.Nested(engineer_serializer.EngineerSchema(exclude=['studio_id', 'studio']))
    client = fields.Nested(client_serializer.ClientSchema(exclude=['password']))
    status = fields.Str()

    class Meta:
        fields = ['start_time', 'end_time', 'studio', 'sound_engineer', 'client', 'status']


class BookingConfirmation(ma.Schema):
    confirm = fields.Boolean(required=True)

    class Meta:
        fields = ['confirm']


booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)
bookings_input_schema = BookingInputSchema()
booking_confirmation_schema = BookingConfirmation()
client_booking_view_schema = BookingViewSchema(many=True, exclude=['client'])
studio_booking_view_schema = BookingViewSchema(many=True, exclude=['studio'])
