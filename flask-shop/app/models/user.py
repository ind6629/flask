from app.db import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    avatar = db.Column(db.String(255), nullable=True)  # 修改为普通文本存储
    
    def set_password(self, password):
        self.password = password  # 直接存储明文密码

    def check_password(self, password):
        return self.password == password  # 直接比较明文密码

    def __repr__(self):
        return '<User {}>'.format(self.username)