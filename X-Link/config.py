# 获取当前文件的绝对路径
import os

root_dir = os.path.dirname(os.path.abspath(__file__))


class Config:
    DEBUG = True
    SECRET_KEY = 'your_secret_key'
    ROOT_DIR = root_dir
    UPLOAD_FOLDER = os.path.join(root_dir, 'upload')
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = './database/TNTDockerPanel.db'
    # 例外认证的路由
    NO_AUTH = ['/system/login', '/system/logout', '/static[*]']
