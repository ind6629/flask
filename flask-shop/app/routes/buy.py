from flask import session, Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models.product import Product
from app.models.cart import Cart
from app.models.order import Order
from app.models.track import TrackCart
from app import db

buy = Blueprint('buy', __name__)
# 添加购物车功能
@buy.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    #购物车记录
    #user_id = 1;  # 假设当前用户ID为1，实际应用中应从session或token中获取
    user_id = session.get('user_id') 
    quantity = int(request.form['quantity']);
    product = Product.query.get_or_404(product_id);
    if product.stock < quantity:
        flash('Not enough stock!')
        return redirect(url_for('main.product_detail', id=product_id));
    cart_item = Cart(
        user_id=user_id, 
        product_id=product_id, 
        quantity=quantity);
    db.session.add(cart_item);
    db.session.commit();
    
    #购物车track记录
    cart_track = TrackCart(
        category = product.category,
        product_id = product.id,
        user_id = user_id);
    db.session.add(cart_track);
    db.session.commit();
    
    flash('Added to cart successfully!')
    return redirect(url_for('main.product_detail', id=product_id,quantity=quantity))
    #return render_template(url_for('main.product_detail', id=product_id))
# 购物车列表功能
@buy.route('/cart')
@login_required
def cart():
    #user_id = 1  # 假设当前用户ID为1，实际应用中应从session或token中获取
    user_id = session.get('user_id') 
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    return render_template('cart.html', cart_items=cart_items)
# 移除购物车功能
@buy.route('/remove_from_cart/<int:cart_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_id):
    cart_item = Cart.query.get_or_404(cart_id)
    db.session.delete(cart_item)
    db.session.commit()
    flash('Removed from cart successfully!')
    return redirect(url_for('buy.cart'))  # 重定向到正确的端点