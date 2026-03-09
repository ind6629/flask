from app import db
from datetime import datetime

class TrackClick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())


class TrackCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(255), nullable=False)  # 假设 product_id 是逗号分隔的字符串
    user_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


    def __repr__(self):
        return f'<Track {self.event_id} - {self.event_type}>'
    
class TrackSearch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=True)
    category = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class TrackOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    product_id = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())