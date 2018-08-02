import json
from flask import (
    Blueprint,
    jsonify,
    request,
    session,
)
import time

from routes import (
    same_user_required,
    xsrf_token_required,
    users_from_content,
)
from models.user import User
from models.reply import Reply
from models.topic import Topic
from models.message import Message
from utils import log, copy_attrs

main = Blueprint('server_reply', __name__)


@main.route('/')
def index():
    tid = request.args['topic_id']
    # page = request.args['page']
    # amount = request.args['amount']
    t = Topic.one(id=tid)
    rs = t.replys
    jsons = [r.json() for r in rs]
    for r in jsons:
        u = User.one(id=r['user_id'])
        r['user'] = copy_attrs([
            'username',
            'avatar',
        ], u)
    log(t, jsons)
    return jsonify(jsons)


@main.route('/add', methods=['POST'])
@xsrf_token_required
def add():
    uid = session.get('user_id')
    if uid is None:
        user = User.guest()
    else:
        user = User.one(id=uid)
        if user is None:
            user = User.guest()

    id = user.id
    form = request.form

    data = {
        'content': form['content'],
        'user_id': id,
        'topic_id': form['topic_id'],
    }
    tid = form.get('target_id')
    if tid is not None:
        data['target_id'] = tid

    r = Reply.new(data)

    # 添加 at 的信息
    users = users_from_content(form['content'])
    for u in users:
        d = {
            'user_id': id,
            'receiver_id': u.id,
            'reply_id': r.id,
            'title': '你被 {} at 了'.format(u.username),
        }
        Message.new(d)

    return jsonify(r.json())


@main.route('/delete')
@same_user_required(Reply)
def delete(id):
    Reply.delete(id)
    return '删除成功'

