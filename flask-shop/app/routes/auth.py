from flask import Blueprint, render_template, redirect, url_for, request, flash, session, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app.models.user import User
from app import db
import os

auth = Blueprint('auth', __name__)

protected_routes = ['main.add_product']
# 路由守卫
@auth.before_request
def before_request():
    if request.endpoint in protected_routes and not current_user.is_authenticated:
        flash('请先登录！', 'warning')
        return redirect(url_for('auth.login'))
# 登录功能
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            session['user_id'] = user.id
            flash('登录成功！', 'success')
            
            user_info = {
                'id': user.id,
                'username': user.username,
            }
            print(user_info)
            
            return jsonify({'status': 'success', 'user': user_info}), 200
        else:
            flash('用户名或密码错误！', 'danger')
            return jsonify({'status': 'error', 'message': '用户名或密码错误！'+password}), 401
            #return jsonify({'status': 'error', 'message': '用户名或密码错误！'}), 401

    
    return render_template('login.html')
# 注册功能
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('用户名或密码已存在', 'danger')
            return render_template('register.html',status = 'fail')

        if password != confirm_password:
            flash('密码不一致！', 'danger')
            return render_template('register.html',status = 'fail')

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        #login_user(new_user)
        #flash('注册成功！', 'success')
        #return redirect(url_for('main.index'))
        return render_template('login.html',status = 'newUser')

    return render_template('register.html',status = 'success')
# 登出功能
@auth.route('/logout')
def logout():
    logout_user()
    session.clear()
    session['user_id'] = -1;
    flash('您已成功登出', 'success')
    return redirect(url_for('main.index'))
# 修改用户信息页面
@auth.route('/user_profile')
@login_required
def user_profile():
    return render_template('user_profile.html', user=current_user)
# 修改用户信息功能
@auth.route('/update_profile', methods=['POST'])
@login_required  
def update_profile():
    user_id = current_user.id
    user = User.query.get(user_id)

    if not user:
        flash('用户不存在', 'error')
        return redirect(url_for('auth.user_profile'))

    existing_user = User.query.filter(
        (User.username == request.form['username']) | (User.email == request.form['email'])
    ).first()
    if existing_user and existing_user.id != user_id:
        flash('用户名或邮箱已存在', 'error')
        return redirect(url_for('auth.user_profile'))

    user.username = request.form['username']
    user.email = request.form['email']

    if 'avatar' in request.files:
        file = request.files['avatar']
        if file and file.filename:
            # 检查文件类型
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
            if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                # 检查文件大小
                max_file_size = 2 * 1024 * 1024  # 2MB
                if len(file.read()) <= max_file_size:
                    file.seek(0)  # 重置文件指针
                    filename = secure_filename(file.filename)
                    
                    # 确保上传目录存在
                    AVATAR_FOLDER = 'flask-shop\\app\\static\\images'
                    # if not os.path.exists(AVATAR_FOLDER):
                    #     os.makedirs(AVATAR_FOLDER)
                    
                    file_path = os.path.join(AVATAR_FOLDER, filename)
                    file.save(file_path)
                    user.avatar = 'static\\images\\'+filename
                else:
                    flash('文件大小超过限制', 'error')
            else:
                flash('不允许的文件类型', 'error')

    db.session.commit()
    flash('用户信息已更新', 'success')
    return redirect(url_for('main.index'))