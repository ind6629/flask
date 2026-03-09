from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, json
from flask_cors import cross_origin
from operator import and_
from app.models.product import Product
from app.models.collection import Collection
from app import db

collect = Blueprint('collect', __name__)

@collect.route('/collection',methods=['post','get'])
def load():
    #获取用户id
    user_id = 1;
    collections = Collection.query.filter(Collection.user_id == user_id).all();
    return render_template('collection.html',collections=collections)

@collect.route('/removeCollection',methods=['post','get'])
def remove():
    #获取用户id
    user_id = 1;
    product_id = int(request.get_json())
    collection = Collection.query.filter(
        and_(
            Collection.user_id == user_id,
            Collection.product_id == product_id
        )
    )
    db.session.delete(collection);
    db.session.commit();
    return jsonify({
        'success': True,
        'message': "已经成功移除"
    })