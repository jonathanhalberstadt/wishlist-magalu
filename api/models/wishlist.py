from api.infrastructure.extensions import db

class Wishlist(db.Model):
    __tablename__ = 'wishlists'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    client = db.relationship("Client", back_populates="wishlists")
    product = db.relationship("Product", back_populates="wishlists")
