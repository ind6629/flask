import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/clothing'   #数据库连接
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # 设置上传文件夹路径
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 限制上传文件大小为2MB
    AVATAR_FOLDER = os.path.join(os.getcwd(), 'avatar')