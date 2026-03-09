from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import numpy as np

app = Flask(__name__)
CORS(app)  # 启用 CORS

def jaccard_similarity(set1, set2):
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0

def item_similarity_matrix(ratings):
    num_items = len(ratings[0])
    similarity_matrix = {}
    for i in range(num_items):
        similarity_matrix[i] = {}
        for j in range(num_items):
            if i == j:
                similarity_matrix[i][j] = 1
                continue
            users_rated_i = {idx for idx, val in enumerate(ratings[:, i]) if val == 1}
            users_rated_j = {idx for idx, val in enumerate(ratings[:, j]) if val == 1}
            similarity_matrix[i][j] = jaccard_similarity(users_rated_i, users_rated_j)
    return similarity_matrix

def itemcf_recommend(ratings, similarity_matrix, user_id, top_n=10):
    user_ratings = ratings[user_id]
    item_scores = {}
    unrated_items = [i for i in range(len(user_ratings)) if user_ratings[i] == 0]
    for item_id in unrated_items:
        score_sum = 0
        similarity_sum = 0
        for other_item_id in range(len(user_ratings)):
            if user_ratings[other_item_id] == 1:
                similarity = similarity_matrix[item_id].get(other_item_id, 0)
                score = 1
                score_sum += similarity * score
                similarity_sum += similarity
        if similarity_sum > 0:
            item_scores[item_id] = score_sum / similarity_sum
    sorted_items = sorted(item_scores.items(), key=lambda x: x[1], reverse=True)
    return [item[0] for item in sorted_items[:top_n]]

@app.route('/my_main/<product_id>', methods=['POST'])
def my_main(product_id):
    # 模拟评分数据，行代表用户，列代表物品，数值为0或1
    # python读取mysql数据库
    import pymysql
    import numpy as np 

    # 连接数据库
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='shop')
    
    # 创建游标对象
    cursor = conn.cursor() 
    # 执行SQL查询

    print("product_id:", product_id)
    
    my_product_id = int(product_id)
    update_sql = ""
    if my_product_id == 100:
        update_sql = "update product_click_matrix_new set apple_click=1 where id=1"
    elif my_product_id == 101:
        update_sql = "update product_click_matrix_new set orange_click=1 where id=1"
    else:
        update_sql = "update product_click_matrix_new set banana_click=1 where id=1"       
    cursor.execute(update_sql)

    cursor.execute("SELECT apple_click, apple_product1_click, apple_product2_click, orange_click, orange_product1_click, orange_product2_click, banana_click, banana_product1_click, banana_product2_click FROM product_click_matrix_new") 

    # 获取查询结果
    result = cursor.fetchall()
    conn.commit()

    ratings_data = np.array(result)

    similarity_matrix = item_similarity_matrix(ratings_data)

    user_id = 0
    recommended_items = itemcf_recommend(ratings_data, similarity_matrix, user_id)

    print("为用户A", user_id, "推荐的物品ID:", recommended_items)

    # 获取推荐list
    str_recommended_items = str(recommended_items).replace("[", "").replace("]", "")
    from datetime import datetime
    # 获取当前时间
    my_now = datetime.now()
    str_my_now = str(my_now)
    
    delete_sql = "delete from track" 
    cursor.execute(delete_sql)
    conn.commit() 

    insert_sql = "insert into track values(1, %s, 1, %s)"         
    cursor.execute(insert_sql, (str_recommended_items, str_my_now))
    conn.commit()
    

    cursor.close()
    conn.close()

    return jsonify(recommended_items)

if __name__ == "__main__":
    app.run(debug=True, port=5001)