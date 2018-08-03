from flask import (
    abort,
    Blueprint,
    jsonify,
    request,
    session,
)

from routes import (
    same_user_required,
    login_required,
    xsrf_token_required,
    get_user_data,
)
from models.user import User
from models.follow import Follow
from utils import log

main = Blueprint('server_follow', __name__)


@main.route('/followed_users/<int:id>')
def followed_users(id):
    """得到当前登陆用户的关注用户"""
    fs = Follow.all(follower_id=id)
    us = [get_user_data(f.user_id) for f in fs]
    return jsonify(us)


@main.route('/followers/<int:id>')
def followers(id):
    fs = Follow.all(user_id=id)
    us = [get_user_data(f.follower_id) for f in fs]
    return jsonify(us)


@main.route('/add', methods=['POST'])
@login_required
@xsrf_token_required
def add():
    json = request.json
    log('follow add:', json)
    uid = json['user_id']
    fid = json['follower_id']
    f = User.one(id=fid)
    if fid != session['user_id']:
        abort(401)
    elif f is None:
        abort(404)
    else:
        d = {
            'user_id': uid,
            'follower_id': fid,
        }
        Follow.new(d)
        return '关注成功'


@main.route('/delete', methods=['POST'])
@xsrf_token_required
def delete():
    json = request.json
    log('follow delete:', json)
    uid = json['user_id']
    fid = json['follower_id']
    f = User.one(id=fid)
    if fid != session['user_id']:
        abort(401)
    elif f is None:
        abort(404)
    else:
        follow = Follow.one(user_id=uid, follower_id=fid)
        Follow.delete(follow.id)
        return '取消关注成功'

