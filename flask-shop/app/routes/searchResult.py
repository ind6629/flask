from operator import and_
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, json
from flask_login import login_required, current_user
from flask_cors import cross_origin
from app.models.track import Track, TrackSearch
from app.models.user import User
from app.models.product import Product
from app.models.cart import Cart
from app.models.order import Order
from app.models.news import News
from app.models.collection import Collection
from app import db
from sqlalchemy.orm import joinedload

searchResult = Blueprint('searchResult', __name__)

@searchResult.route('/result', methods=['GET', 'POST'])
def load():
    curr_user_id = request.args.get('user_id');
    keyword = request.args.get('keyword');
    products = Product.query.filter(Product.name.ilike(f'%{keyword}%')).all()
    dict_data = [{
        'product_id' : item.id,
        'category': item.category,
    } for item in products]
    # keywords = {};
    # for itme in dict_data:
    #     category = itme['category'];
        # if category in keywords:
        #     keywords[category] = keywords[category]+1;
        # else:
        #     keywords[category] = 1;
    # print('---搜索内容关键字统计---');
    # print(keywords);
    # print('---排序后---');
    # sorted_keywords = sorted(keywords.items(), key=lambda x: x[1],reverse = True)
    # print(sorted_keywords)
    for itme in dict_data:
        track_serach = TrackSearch(
            product_id=itme['product_id'],
            user_id=curr_user_id,
            category=itme['category']
        )
        db.session.add(track_serach)
    db.session.commit()
        
    if len(keyword) == 0:
        keyword = "any"
    
    return render_template('searchResult.html',products=products,keyword = keyword)