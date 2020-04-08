from app import db


class Studio(db.Model):
    __tablename__ = 'studio'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    def __repr__(self):
        studio_object = {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }