from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from datetime import timedelta

import config

from models import db
from models.reply import Reply
from models.topic import Topic
from models.user import User

from utils import log

# 注册蓝图
from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.user import main as user_routes
from routes.reply import main as reply_routes
from routes.message import main as message_routes
from routes.board import main as board_routes
from routes.follow import main as follow_routes

import config

def configured_app():
    app = Flask(__name__)
    # 设置 secret_key 来使用 flask 自带的 session
    app.secret_key = config.secret_key
    # session 不设置时间的话，permernent 默认是 一个月时间
    # app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{}@localhost/phoe?charset=utf8mb4'.format(config.database_password)
    db.init_app(app)


    # module = __import__('routes.index')
    # b = getattr(getattr(module, 'index'), 'blueprint')()
    # log('index blueprint', b)
    # app.register_blueprint(b)
    # log('url map', app.url_map)
    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(user_routes, url_prefix='/user')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(message_routes, url_prefix='/message')
    app.register_blueprint(board_routes, url_prefix='/board')
    app.register_blueprint(follow_routes, url_prefix='/follow')

    # 管理界面
    admin = Admin(app, name='phoe', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Topic, db.session))
    admin.add_view(ModelView(Reply, db.session))

    return app


# 运行代码
if __name__ == '__main__':
    # app.add_template_filter(count)
    # debug 模式可以自动加载代码的变动, 不用重启程序
    app = configured_app()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2000,
    )
    app.run(**config)
