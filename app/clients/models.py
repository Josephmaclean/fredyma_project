from app import db, ma


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(12), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)


class ClientSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'phone_number']


client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)
