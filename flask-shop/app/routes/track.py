from flask import Blueprint, request, flash, request, jsonify, render_template
from app.models.track import TrackClick, TrackCart, Track
from app import db

track = Blueprint('track', __name__)

# 数据埋点
@track.route('/api/tracking', methods=['POST'])
def track_event():
    data = request.get_json()
    event_id = data.get('event_id')
    event_type = data.get('event_type')
    user_id = data.get('user_id')
    category = data.get('category')

    # 创建并保存 TrackClick 记录
    track_click = TrackClick(
        event_id=event_id,
        event_type=event_type,
        user_id=user_id,
        category=category,
    )
    db.session.add(track_click)
    db.session.commit()

    return jsonify({"status": "success"}), 200


