from app import db
from app.models.user import User
from app.models.product import Product

#模型定义结构:购物车
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    #关系映射
    user = db.relationship('User', backref=db.backref('carts', lazy=True))
    product = db.relationship('Product', backref=db.backref('carts', lazy=True))

    def __repr__(self):
        return '<Cart {}>'.format(self.id)