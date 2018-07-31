from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from datetime import timedelta

import config

from models import db
from models.topic import Topic

from utils import log

# 注册蓝图
# 有一个 url_prefix 可以用来给蓝图中的每个路由加一个前缀
# import routes.index as index_view
from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.user import main as user_routes
# from routes.reply import main as reply_routes

import config


def count(input):
    log('count using jinja filter')
    return len(input)


def time_format(milliseconds):
    log('time_format using jinja filter')
    return '{} 毫秒'.format(milliseconds)


def check_signature(s):
    s = s.strip()
    if len(s) == 0:
        s = '这家伙很懒，什么个性签名都没有留下。'
    return s


def configured_app():
    app = Flask(__name__)
    # 设置 secret_key 来使用 flask 自带的 session
    # 这个字符串随便你设置什么内容都可以
    app.secret_key = config.secret_key
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
    # app.register_blueprint(reply_routes, url_prefix='/reply')

    app.template_filter()(count)
    app.template_filter()(time_format)
    app.template_filter()(check_signature)

    admin = Admin(app, name='phoe', template_mode='bootstrap3')
    # admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Topic, db.session))
    # admin.add_view(ModelView(Reply, db.session))
    # Add administrative views here

    return app


# 运行代码
if __name__ == '__main__':
    # app.add_template_filter(count)
    # debug 模式可以自动加载代码的变动, 不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    app = configured_app()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2000,
    )
    app.run(**config)
