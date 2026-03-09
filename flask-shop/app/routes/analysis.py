from datetime import datetime, timedelta

from app import db
from app.models.cart import Cart
from app.models.collection import Collection
from app.models.news import News
from app.models.order import Order
from app.models.product import Product
from app.models.track import TrackClick, TrackSearch, TrackCart, TrackOrder
from app.models.user import User
from flask import Blueprint, render_template
from sqlalchemy import func

analysis = Blueprint('analysis', __name__)
# 商品列表
@analysis.route('/analysis')
def init():
    return render_template('analysis.html');

@analysis.route('/clickData')
def clickData():
    # clickTracks = TrackClick.query.with_entities(TrackClick.user_id, TrackClick.event_id).all()
    # product_ids = sorted({pid for (_, pid) in clickTracks}, key=int)
    product_interaction_counts = (
    TrackClick.query
    .with_entities(
        TrackClick.event_id,
        func.count(TrackClick.user_id).label('interaction_count')  # 计算总交互次数
    )
    .group_by(TrackClick.event_id)
    .order_by(TrackClick.event_id)
    .all())
    data = [row._asdict() for row in product_interaction_counts]
    for item in data:
        product_id = item['event_id'];
        product = Product.query.filter(Product.id == product_id).first();
        item['name'] = product.name;
    # print("---product_interaction_counts---");
    # print(data);
    return render_template('table_clickData.html',data = data);

@analysis.route('/searchData')
def searchData():
    keywords_search_counts = (
    TrackSearch.query
    .with_entities(
        TrackSearch.category,
        func.count(TrackSearch.id).label('search_count')  # 计算总交互次数
    )
    .group_by(TrackSearch.category)
    .all())
    data = [row._asdict() for row in keywords_search_counts]
    print("---keywords_search_counts---");
    print(data);
    return render_template('table_searchData.html',data = data);

@analysis.route('/cartData')
def cartData():
    cart_category_counts = (
    TrackCart.query
    .with_entities(
        TrackCart.category,
        func.count(TrackCart.id).label('count')  # 计算总交互次数
    )
    .group_by(TrackCart.category)
    .all())
    data = [row._asdict() for row in cart_category_counts]
    print("---cart_category_counts---");
    print(data);
    return render_template('table_cartData.html',data = data);

@analysis.route('/orderData')
def orderData():
    # 获取当前日期和7天前的日期
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    # 查询近7天每天的最高频category
    result = db.session.query(
        func.date(TrackOrder.timestamp).label('date'),  # 提取日期部分
        TrackOrder.category,
        func.count(TrackOrder.category).label('count')  # 统计分类出现次数
    ).filter(
        TrackOrder.timestamp >= start_date,
        TrackOrder.timestamp <= end_date,
        TrackOrder.category.isnot(None)  # 排除category为NULL的记录
    ).group_by(
        func.date(TrackOrder.timestamp),  # 按日期分组
        TrackOrder.category
    ).order_by(
        func.date(TrackOrder.timestamp).asc(),  # 按日期升序
        func.count(TrackOrder.category).desc()  # 按计数降序
    ).all()

    # 提取每天的最高频category
    daily_top_categories = {}
    for row in result:
        date_str = row.date.strftime('%Y-%m-%d')
        if date_str not in daily_top_categories:  # 只保留每天的第一个结果（即最高频）
            daily_top_categories[date_str] = {
                'category': row.category,
                'count': row.count
            }

    # 输出结果
    # print("近七天每天的最高频分类：")
    list_data=[];
    for date, data in daily_top_categories.items():
        #print(f"{date}: {data['category']} (出现次数: {data['count']})")
        list_data.append({
        "category": data['category'],
        "date": date,
        "count": data['count']
        })
    # print("---list_data---");
    # print(list_data);
    return render_template('table_orderData.html',data = list_data);

@analysis.route('/otherData')
def otherData():
    return render_template('table_otherData.html');