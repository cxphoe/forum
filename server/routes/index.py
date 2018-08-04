from flask import (
    abort,
    Blueprint,
    jsonify,
    make_response,
    send_from_directory,
    session,
    redirect,
    request,
)
import uuid

from routes import get_user_data

from models.user import User
from models.follow import Follow
from utils import log

main = Blueprint('index', __name__)

@main.route('/current-user')
def current_user():
    # 从 session 中找到 user_id 字段, 找不到就 -1
    # 然后用 id 找用户
    # 找不到就返回 None
    uid = session.get('user_id', -1)
    u = User.one(id=uid)
    if u is not None:
        ts = u.topics
        involved_ts_count = u.involved_ts_count()
        fs = Follow.all(user_id=u.id)
        followeds = Follow.all(follower_id=u.id)
        data = {
            'id': u.id,
            'avatar': u.avatar,
            'username': u.username,
            'topic_count': len(ts),
            'involved_count': involved_ts_count,
            'follower_count': len(fs),
            'followed_ids': [f.user_id for f in followeds],
        }
    else:
        g = User.guest()
        data = {
            'id': g.id,
            'avatar': g.avatar,
            'username': g.username,
            'is_guest': True,
        }
    resp = make_response(jsonify(data), 200)

    # 设置 xsrf token
    token = uuid.uuid4()
    token = bytes(str(token), encoding='utf-8')
    resp.set_cookie('_xsrf', token, httponly=True)
    resp.headers['token'] = token
    return resp


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User.validate_signin(form)

    if u is None:
        # 返回 404
        response = make_response('用户名或密码错误', 404)        
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        user = {
            'id': u.id,
            'avatar': u.avatar,
            'username': u.username,
        }
        response = make_response(jsonify(user), 200)
    return response


@main.route('/logout')
def logout():
    uid = session.get('user_id', -1)
    u = User.one(id=uid)

    if u is None:
        response = make_response('当前无用户！', 404)
    else:
        del session['user_id']
        response = make_response('登出成功！', 200)
    return response


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    u = User.register(form)
    if u is None:
        response = make_response('注册失败！', 404)
    else:
        response = make_response('注册成功！', 200)
    return response


@main.route('/images/<filename>')
def image(filename):
    # 不能直接拼接路由，不安全，比如
    # open(os.path.join('images', filename), 'rb').read()
    return send_from_directory('images', filename)
