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

from models.user import User
from utils import log

main = Blueprint('user', __name__)

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
