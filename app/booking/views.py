import json, datetime
from flask import Blueprint, Response, abort, request
from app.clients import (permissions as client_permissions,
                         models as client_models)
from app.studio import (permissions as studio_permissions,
                        models as studio_models)
from app import db

from .models import Booking
from .serializers import (bookings_input_schema, booking_schema,
                          booking_confirmation_schema)

bookings = Blueprint('booking', __name__)


@bookings.route('/booking/new', methods=['POST'])
@client_permissions.client_login_required
def book_session(user_id):
    errors = bookings_input_schema.validate(request.json)
    if errors:
        return abort(Response(json.dumps(errors), 400, mimetype='application/json'))

    client = client_models.Client.query.get(user_id)
    if client is None:
        message = {
            'error': 'Client does not exist'
        }
        return abort(Response(json.dumps(message), 400,
                              mimetype='application/json'))

    details = request.json
    studio_id = details['studio_id']
    session_type = details['session_type']

    start_time = datetime.datetime.strptime(f"{details['date']} {details['start_time']}",
                                            '%Y-%m-%d %H:%M')
    end_time = datetime.datetime.strptime(f"{details['date']} {details['end_time']}",
                                          '%Y-%m-%d %H:%M')

    if end_time > start_time:
        message = {
            'error': 'booking end time cannot be greater than booking start time'
        }
        abort(Response(json.dumps(message), 400, mimetype='application/json'))

    new_booking = Booking(studio_id=studio_id, start_time=start_time,
                          end_time=end_time, session_type=session_type,
                          client_id=user_id, status='pending')

    db.session.add(new_booking)
    db.session.commit()

    return Response(booking_schema.dumps(new_booking), 201,
                    mimetype='application/json')


@bookings.route('/booking/<int:booking_id>/status/update', methods=['POST'])
@studio_permissions.studio_login_required
def confirm_booking(booking_id, user_id):
    errors = booking_confirmation_schema.validate(request.json)
    if errors:
        return abort(Response(json.dumps(errors), 400, mimetype='application/json'))

    confirmation = request.json['confirmation']
    booking = Booking.query.filter_by(id=booking_id, studio_id=user_id).first()
    if booking is None:
        message = {
            'error': 'Booking not found'
        }
        return abort(Response(json.dumps(message), 404, mimetype='application/json'))
    booking.status = confirmation
    db.session.commit()
    message = {
        'message': 'booking status updated'
    }
    return Response(json.dumps(message), 200, mimetype='application/json')