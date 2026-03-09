from operator import and_
from flask import session, Blueprint, render_template, redirect, url_for, request, flash, jsonify, json
from flask_login import login_required, current_user
from flask_cors import cross_origin
from app.models.track import Track
from app.models.user import User
from app.models.product import Product
from app.models.cart import Cart
from app.models.order import Order
from app.models.news import News
from app.models.collection import Collection
from app import db
from sqlalchemy.orm import joinedload

order = Blueprint('order', __name__)

@order.route('/order')
def load():
    #获取当前用户id
    #user_id = 1
    user_id = session.get('user_id') 
    orders = Order.query.filter(Order.user_id == user_id).all();
    return render_template('order.html',orders = orders)

@order.route('/cancelOrder', methods=['POST'])
def cancelOrder():
    ids = request.get_json()
    orders = Order.query.filter(Order.id.in_(ids)).all()
    for order in orders:
        db.session.delete(order)
    db.session.commit()
    flash("所选订单内容已成功移除")
    return jsonify({
            'success': True,
            'message': '成功删除{}个订单'.format(len(ids))
        })

@order.route('/settleOrder', methods=['POST'])
def settleOrder():
    ids = request.get_json()
    orders = Order.query.filter(Order.id.in_(ids)).all()
    totalPrice = 0;
    for order in orders:
        totalPrice += int(order.total_price);
        db.session.delete(order)
        
    db.session.commit()
    #待计算价格，下一步措施什么的
    flash("所选订单内容已成功计算")
    return jsonify({
            'success': True,
            'message': '成功结算{}个订单,总价为：{}'.format(len(ids),totalPrice)
        })