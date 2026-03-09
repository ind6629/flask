from app import db
from datetime import datetime
from app.models.user import User
from app.models.product import Product

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    rating = db.Column(db.Integer)

    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    product = db.relationship('Product', backref='comments_ref', lazy=True)

    def __repr__(self):
        return f'<Comment {self.content[:20]}...>'