from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models.product import Product
from app.models.comment import Comment
from app import db
from flask_login import current_user, login_required

comments = Blueprint('comments', __name__)

# 添加评论功能
@comments.route('/comment/<int:product_id>', methods=['POST'])
@login_required
def add_comment(product_id):
    comment_content = request.form['comment']
    product = Product.query.get(product_id)
    if product:
        comment = Comment(user_id=current_user.id, product_id=product_id, content=comment_content)
        db.session.add(comment)
        db.session.commit()
        flash('评论已成功提交！')
    else:
        flash('产品不存在，无法提交评论。')
    return redirect(url_for('main.product_detail', id=product_id))

    #return redirect(url_for('main.product_detail'))