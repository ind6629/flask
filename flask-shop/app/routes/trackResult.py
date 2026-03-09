from flask import Blueprint, request, flash, request, jsonify, render_template
from app.models.track import TrackClick, TrackCart, Track
from app.models.product import Product
from app import db
import numpy as np
from collections import defaultdict

trackResult = Blueprint('trackResult', __name__)

# 数据埋点
@trackResult.route('/api/trackResult', methods=['POST'])
def track_result():
    data = request.get_json();
    curr_user_id = data.get('user_id');
    trackClicks = TrackClick.query.all();
    track_clicks_data = [];
    for item in trackClicks:
        user_id = item.user_id;
        product_id = item.event_id;
        track_clicks_data.append({'user_id' : user_id,'product_id' : product_id});
    product_ids = recommend(track_clicks_data,curr_user_id);
    
    recommend_products = []
    for product_id in product_ids:
        product = Product.query.filter(Product.id==product_id).first()
        if product:
            recommend_products.append({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'stock': product.stock,
                'image': product.image,
                'category': product.category
            })
    #print('recommend_products:',recommend_products);


    return jsonify({"status": "success","data":recommend_products});

def recommend(data,curr_user_id):
    # 构建物品-用户倒排表
    item_users = defaultdict(set)
    for item in data:
        item_users[item['product_id']].add(item['user_id'])

    # 计算Jaccard相似度
    items = list(item_users.keys())
    n = len(items)
    sim_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i == j:
                sim_matrix[i][j] = 1.0  # 对角线为1
            else:
                item_i = items[i]
                item_j = items[j]
                users_i = item_users[item_i]
                users_j = item_users[item_j]

                intersection = len(users_i & users_j)
                union = len(users_i | users_j)

                sim_matrix[i][j] = intersection / union if union > 0 else 0
    # print("物品列表:", items)
    # print("Jaccard相似度矩阵:")
    # print(sim_matrix)
    # print(data);
    # 转换为物品名对应的相似度字典
    item_sim = defaultdict(dict)
    for i in range(n):
        for j in range(n):
            item_sim[items[i]][items[j]] = sim_matrix[i][j]
    print('item_sim:',item_sim)
            
    # 获取用户历史交互物品
    user_id = curr_user_id;
    user_items = set()
    for item in data:
        if item['user_id'] == user_id:
            user_items.add(item['product_id'])
    print('user_items',user_items)
    
    # 计算推荐得分
    scores = defaultdict(float)
    for interacted_item in user_items:
        for candidate_item, similarity in item_sim[interacted_item].items():
            if candidate_item not in user_items:  # 排除已交互物品
                scores[candidate_item] += similarity
    recommendResult = sorted(scores.items(), key=lambda x: -x[1]);
    recommend_items = [item for item, score in recommendResult]
    #print('recommendResult:',recommendResult);
    #print('recommend_items:',recommend_items);
    return recommend_items;