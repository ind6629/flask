from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from app.db import db  # 从 db.py 导入 db 对象
from app.models.user import User  # 导入 User 类

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/shop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化 Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # 设置登录视图

def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app, resources={r"/": {"origins": "http://localhost:8080"}})  # 允许来自 http://localhost:8080 的请求
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)

    # 注册蓝图
    from app.routes.main import main
    app.register_blueprint(main)

    from app.routes.auth import auth
    app.register_blueprint(auth)

    from app.routes.buy import buy
    app.register_blueprint(buy)
    
    from app.routes.comments import comments
    app.register_blueprint(comments)
    
    from app.routes.track import track
    app.register_blueprint(track)
    
    from app.routes.order import order
    app.register_blueprint(order)
    
    from app.routes.collect import collect
    app.register_blueprint(collect)
    
    from app.routes.searchResult import searchResult
    app.register_blueprint(searchResult)
    
    from app.routes.trackResult import trackResult
    app.register_blueprint(trackResult)
    
    from app.routes.analysis import analysis
    app.register_blueprint(analysis)
    
    # from app.routes.dataAnalysis import dataAnalysis
    # app.register_blueprint(dataAnalysis)
    # 用户加载回调
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app