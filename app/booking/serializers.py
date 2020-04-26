import datetime
from app import ma
from marshmallow import fields, validate, validates
from marshmallow.exceptions import ValidationError


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
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)
    date = fields.Date(required=True)

    @validates('start_time')
    def validate_start_time(self, value):
        time_now = datetime.datetime.utcnow().time()
        start_time = datetime.datetime.strptime(value, '%H:%M').time()

        if time_now > start_time:
            raise ValidationError('invalid start time')

    @validates('end_time')
    def validate_end_time(self, value):
        start_time = datetime.datetime.strptime(value, '%H:%M')
        end_time = datetime.datetime.strptime(self.start_time, '%H:%M')
        if end_time > start_time:
            raise ValidationError('end time must be greater than start time')

    class Meta:
        fields = ['id', 'studio_id', 'client_id', 'start_time', 'end_time']


booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)
bookings_input_schema = BookingSchema(exclude=['client_id', 'status'])
