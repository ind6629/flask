from app import db
from app.models.product import Product
from app.models.user import User

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('collections', lazy=True))
    product = db.relationship('Product', backref=db.backref('collections', lazy=True))

    def __repr__(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id
        }