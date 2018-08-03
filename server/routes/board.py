from flask import (
    Blueprint,
    jsonify,
)

from models.board import Board
from utils import log

main = Blueprint('server_board', __name__)


@main.route('/')
def index():
    bs = Board.all()
    jsons = []
    for b in bs:
        j = b.json()
        j['topic_count'] = len(b.topics)
        jsons.append(j)
    return jsonify(jsons)


@main.route('/topics/<int:id>')
def topics(id):
    b = Board.one(id=id)
    ts = b.topics
    jsons = [t.json() for t in ts]
    return jsonify(jsons)

