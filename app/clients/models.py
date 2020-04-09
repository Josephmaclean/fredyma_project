from app import db, ma

client_studio = db.Table('client_studio',
                         db.Column('client_id', db.Integer, db.ForeignKey('client.id'), primary_key=True),
                         db.Column('studio_id', db.Integer, db.ForeignKey('studio.id'), primary_key=True)
                         )


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(12), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    studios = db.relationship('Studio', secondary=client_studio, lazy='subquery',
                              backref=db.backref('clients', lazy=True))


class ClientSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'phone_number']


client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)
