import os
from threading import current_thread
from flask import Flask
from config import Config
from .tools import register_blueprints
from .tools import NoraORM
from werkzeug.exceptions import HTTPException
from .middleware import before_request, after_request, teardown_request, teardown_appcontext, errorhandler


def create_app():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(Config)
    app.static_folder = app.config['UPLOAD_FOLDER']
    # 初始化数据库类实例
    db_instance = NoraORM(app.config['SQLALCHEMY_DATABASE_URI'])
    # 将数据库类实例保存到 Flask 应用的配置中
    app.config['db_instance'] = db_instance

    # 注册请求相关的钩子
    @app.before_request
    def before_request_func():
        before_request(app.config['NO_AUTH'])

    app.after_request(after_request)
    # app.teardown_request(teardown_request)
    app.teardown_appcontext(teardown_appcontext)

    # app.errorhandler(errorhandler)
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return errorhandler(e)

    # 在teardown_appcontext钩子中关闭数据库连接
    @app.teardown_appcontext
    def teardown_appcontext_func(exception):
        teardown_request()

    # 自动注册蓝图
    register_blueprints(app, 'api.controller', os.path.join(app.root_path, 'controller'))
    # 可以在这里初始化数据库

    return app
