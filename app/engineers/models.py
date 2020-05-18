import json
from app import db


class Engineers(db.Model):
    """
    Engineer model
    model representing sound engineers
    """
    __tablename__ = 'sound_engineer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    studio_id = db.Column(db.Integer, db.ForeignKey('studio.id'), nullable=False)
    bookings = db.relationship('Booking', backref='sound_engineer', lazy=True)

    def __repr__(self):
        engineer_object = {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'studio_id': self.studio_id
        }

        return json.dumps(engineer_object)
