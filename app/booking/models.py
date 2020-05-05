import enum, json
from app import db


class SessionType(enum.Enum):
    short = '30 minutes'
    medium = '60 minutes'
    long = '2 hours'


class Status(enum.Enum):
    confirmed = 'Confirmed'
    pending = 'Pending'
    declined = 'Declined'


class Booking(db.Model):
    """
    Booking model
    model representing the booking of studio sessions
    fields = [id, studio, start_time, end_time, status, client, session_type]
    """
    __tablename__ = 'booking'

    id = db.Column(db.Integer, primary_key=True)
    studio_id = db.Column(db.Integer, db.ForeignKey('studio.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    session_type = db.Column(db.Enum(SessionType, name='session_type'))
    status = db.Column(db.String(), default='pending', nullable=False)
    sound_engineer_id = db.Column(db.Integer, db.ForeignKey('sound_engineer.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('studio_id', 'start_time', 'sound_engineer_id'),
    )

    def __repr__(self):
        booking_object = {
            'id': self.id,
            'studio_id': self.studio_id,
            'client_id': self.client_id,
            'status': self.status
        }
        return json.dumps(booking_object)