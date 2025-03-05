from api.infrastructure.extensions import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String)
    brand = db.Column(db.String)
    url = db.Column(db.String)
    title = db.Column(db.String, nullable=False)
    review_score = db.Column(db.Float)

    wishlists = db.relationship("Wishlist", back_populates="product")
