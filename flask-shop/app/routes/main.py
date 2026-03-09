from operator import and_
from flask import session, Blueprint, render_template, redirect, url_for, request, flash, jsonify, json
from flask_login import login_required, current_user
from flask_cors import cross_origin
from app.models.track import Track, TrackOrder
from app.models.user import User
from app.models.product import Product
from app.models.cart import Cart
from app.models.order import Order
from app.models.news import News
from app.models.collection import Collection
from app import db
from sqlalchemy.orm import joinedload

main = Blueprint('main', __name__)
# 商品列表
@main.route('/')
def index():
    #products = Product.query.all()
    track_results = Track.query.with_entities(Track.user_id, Track.product_id).all()
    
    # 也可以用filter（适合更复杂的条件）
    phones = Product.query.filter(Product.type == 'ladieswear').all();
    computers = Product.query.filter(Product.type == 'menswear').all();
    appliances = Product.query.filter(Product.type == 'jewelry').all();
    components = Product.query.filter(Product.type == 'watch').all();
    #获取用户id
    #user_id = 1;
    user_id = session.get('user_id') 
    Carts = (Cart.query.filter(Cart.user_id == user_id).options(joinedload(Cart.product)).all());
    news = News.query.all();

    track_data = []
    matching_product_ids = []

    for track in track_results:
        product_ids = track.product_id.split(',')
        
       
        for product_id in product_ids:
            product = Product.query.filter_by(id=product_id).first()
            if product:
                track_data.append({
                    'product_id': product_id,
                    'user_id': track.user_id,
                    'name': product.name,
                    'image': product.image,
                    'stock': product.stock,
                    'price': product.price
                })
        
    # local_user_info = request.headers.get('X-User-Info')
    # if local_user_info:
    #     local_user_info = json.loads(local_user_info)
    #     local_user_id = local_user_info.get('id')
    # else:
    #     local_user_id = None

    # filtered_data = [track for track in track_data if track['user_id'] == local_user_id]

    # matching_product_ids = [track['product_id'] for track in filtered_data]

    # print(matching_product_ids)
    

    return render_template('home.html',phones=phones,computers=computers,appliances=appliances, components=components, track_data=track_data,news=news,matching_product_ids=matching_product_ids,Carts=Carts)
    # return jsonify([product.to_dict() for product in products])  
# 帮助页面
@main.route('/help')
@cross_origin()  
def help():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])  
# # 关于页面
@main.route('/about')
def about():
    return render_template('about.html')
# # 大模型页面
# @main.route('/aichat')
# def aichat():
#     return render_template('nongxiaoling.html')
# 商品详情页面
@main.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    #获取userID
    user_id = 1;
    is_collected = Collection.query.filter(
        and_(
            Collection.user_id == user_id,
            Collection.product_id == id
        )
    ).first() is not None
    return render_template('product_detail.html', product=product,user_id = user_id,is_collected = is_collected)
# # 搜索商品功能
# @main.route('/search_product',methods=['GET','POST'])
# def search_product():
#     if request.method == 'POST':
#         search_query = request.form['search']
#         products = Product.query.filter(Product.name.like(f'%{search_query}%')).all()
#         return render_template('home.html', products=products)
    
# 分类按钮功能
@main.route('/category', methods=['GET', 'POST'])
def category():
    fixed_value = request.args.get('fixed_value', '')
    products = Product.query.filter(Product.category.like(f'%{fixed_value}%')).all()

    print(f"查询条件: {fixed_value}")
    print(f"查询结果: {products}")

    return render_template('home.html', products=products)
# 添加商品功能
@main.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        image = request.form['image']
        stock = int(request.form['stock'])
        description = request.form['description']

        new_product = Product(name=name, price=price, image=image, stock=stock, description=description)
        db.session.add(new_product)
        db.session.commit()

        flash('Product added successfully!')
        return redirect(url_for('main.index'))

    return render_template('add_product.html')
# 修改商品功能
@main.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    # product = Product.query.get_or_404(product_id) 
    
    # if request.method == 'POST':
    #     product.name = request.form['name']
    #     product.price = float(request.form['price'])
    #     product.image = request.form['image']
    #     product.stock = int(request.form['stock'])
    #     product.description = request.form['description']

    #     db.session.commit()  # 提交更改到数据库

    #     flash('Product updated successfully!')
    #     return redirect(url_for('main.index',id=product_id))

    # 如果请求方法为 GET，则显示编辑页面并预填现有数据
    #return render_template('edit_product.html', product=product)
    return render_template('edit_product.html')
# # 删除商品功能
# @main.route('/delete_product/<int:product_id>', methods=['POST'])
# @login_required
# def delete_product(product_id):
#     product = Product.query.get_or_404(product_id)
    
#     orders = Order.query.filter_by(product_id=product_id).all()
#     for order in orders:
#         db.session.delete(order)
    
#     db.session.delete(product)
#     db.session.commit()
    
#     flash('Product deleted successfully!')
#     return redirect(url_for('main.index'))
# 购物车结算功能
@main.route('/checkout', methods=['get','POST'])
@login_required
def checkout():
    user_id = session.get('user_id') 
    #user_id = 1  # 假设当前用户ID为1，实际应用中应从session或token中获取
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    for cart_item in cart_items:
        total_price = cart_item.product.price * cart_item.quantity
        order = Order(user_id=user_id, product_id=cart_item.product_id, quantity=cart_item.quantity, total_price=total_price)
        db.session.add(order)
        product = Product.query.get(cart_item.product_id)
        product.stock -= cart_item.quantity
        db.session.delete(cart_item)
        order_track = TrackOrder(
            user_id = user_id,
            product_id = product.id,
            category = product.category
        );
        db.session.add(order_track);
    
    db.session.commit()
    flash('Order placed successfully!')
    return redirect(url_for('main.index'))
# 直接结算
@main.route('/addOrder', methods=['get','POST'])
@login_required
def addOrder():
    user_id = session.get('user_id') 
    #user_id = 1  # 假设当前用户ID为1，实际应用中应从session或token中获取
    product_id = request.args.get('product_id', type=int)
    product_price = request.args.get('product_price', type=float)
    quantity = request.args.get('quantity', type=int)
    total_price = product_price*quantity;
    order = Order(user_id=user_id,product_id=product_id,quantity=quantity,total_price=total_price);
    db.session.add(order)
    product = Product.query.get(product_id)
    product.stock -= quantity
    db.session.commit()
    return redirect(url_for('order.load'))
# # 新闻列表功能
# @main.route('/content', methods=['GET'])
# def content():
#     page = request.args.get('id', 'default')
#     page_items = News.query.filter_by(id=page).all()
#     return render_template('content.html', page_items=page_items)

    

# 添加收藏功能
@main.route('/collect/<int:user_id>,<int:product_id>,<string:is_collected>', methods=['get','POST'])
def collect(user_id,product_id,is_collected):
    if is_collected == 'True':
        collection = Collection.query.filter(
            Collection.user_id == user_id,
            Collection.product_id == product_id
        ).first()
        db.session.delete(collection)
    else:
        collection = Collection(product_id = product_id,user_id = user_id);
        db.session.add(collection)
        flash('商品收藏成功!')
    db.session.commit()
    
    return product_detail(product_id);

