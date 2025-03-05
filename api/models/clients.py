from api.infrastructure.extensions import db

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    wishlists = db.relationship("Wishlist", back_populates="client")

    @staticmethod
    def get_by_email(email):
        return Client.query.filter_by(email=email).first()
