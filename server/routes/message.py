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
    login_required,
    xsrf_token_required,
    get_user_data,
)
from models.user import User
from models.message import Message
from utils import log

main = Blueprint('server_message', __name__)


@main.route('/')
@login_required
@xsrf_token_required
def index():
    """得到当前登陆用户收到的信息"""
    uid = session['user_id']
    ms = Message.all(receiver_id=uid)
    jsons = [m.json() for m in ms]
    for j in jsons:
        u = User.one(id=j['user_id'])
        j['avatar'] = u.avatar
    return jsonify(jsons)


@main.route('/add', methods=['POST'])
def add():
    pass


@main.route('/delete')
@same_user_required(Message)
def delete(id):
    Message.delete(id)
    return '删除成功'

