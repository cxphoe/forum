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

from routes import processImg
from models.user import User
from utils import log

main = Blueprint('server_user', __name__)

@main.route('/<int:id>')
def user(id):
    u = User.one(id=id)
    if u is None:
        abort(404)
    else:
        data = {
            'id': u.id,
            'avatar': u.avatar,
            'username': u.username,
        }
        return jsonify(data)


@main.route('/detail/<int:id>')
def user_detail(id):
    u = User.one(id=id)
    if u is None:
        abort(404)
    else:
        topics = [t.json() for t in u.topics]
        for t in topics:
            t['pulished'] = True
        data = {
            'id': u.id,
            'avatar': u.avatar,
            'username': u.username,
            'topics': topics
        }
        return jsonify(data)


@main.route('/update/<int:id>', methods=['POST'])
def user_update(id):
    uid = session.get('user_id')
    if uid == id:
        # 更新user的数据
        form = request.form.to_dict()
        files = request.files
        avatar= files.get('avatar')
        if avatar is not None:
            url = processImg(avatar)
            form['avatar'] = url
        log('update data:', form)
        u = User.one(id=uid)
        for k, v in form.items():
            setattr(u, k, v)
        u.save()
        resp = make_response('设置成功', 200)
    else:
        resp = make_response('认证失败，无法设置', 401)
    return resp
