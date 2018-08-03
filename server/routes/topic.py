import json
from flask import (
    abort,
    Blueprint,
    jsonify,
    make_response,
    request,
    session,
)
import time

from routes import (
    processImg,
    same_user_required,
    xsrf_token_required,
    get_user_data,
)
from models.topic import Topic
from models.reply import Reply
from models.board import Board
from utils import log

main = Blueprint('server_topic', __name__)


@main.route('/')
def index():
    jsons = Topic.all_json()
    for j in jsons:
        tid = j['id']
        rs = Reply.all(topic_id=tid)
        # 回复的数量
        j['reply_count'] = len(rs)
        # 话题发布用户的信息
        j['user'] = get_user_data(j['user_id'])
        # 话题所属的板块
        b = Board.one(id=j['board_id'])
        j['board_name'] = b.name
    return jsonify(jsons)


@main.route('/<int:id>')
def detail(id):
    t = Topic.get(id)
    json = t.json()
    json['user'] = get_user_data(t.user_id)
    b = Board.one(id=json['board_id'])
    json['board_name'] = b.name
    return jsonify(json)


def process_content_data(data, files):
    get_content = {
        'text': lambda item: item['data'],
        'image': lambda item: '<img src="{}">'.format(processImg(files[item['name']])),
    }

    log(files, data['content'])
    content_parts = []
    for item in data['content']:
        content_parts.append(get_content[item['type']](item))
    data['content'] = '\n'.join(content_parts)


@main.route('/add', methods=['POST'])
def add():
    """ 接受到的是一个特殊的数据结构：
    request.files 接受到的是文章内容中上传的图片(图片名和文件的键值对)
    request.form['data']['content'] 接受到的数据是一个数组，成员的结构可能是：
        { 'type': 'text', 'data': 文本值 }
        { 'type': 'img', 'name': 文件名字（用于在 request.files 中查找文件）, 'data': 图片src }
    """
    files = request.files
    form = request.form

    data = json.loads(form['data'])
    process_content_data(data, files)

    uid = form['user_id']
    bid = form['board_id']

    t = Topic.new(data, uid, bid)
    t.save()

    return ''


@main.route('/delete/<int:id>')
@xsrf_token_required
@same_user_required(Topic)
def delete(id):
    Topic.delete(id)
    return make_response('删除成功', 200)


@main.route('/update/<int:id>', methods=['POST'])
@xsrf_token_required
@same_user_required(Topic)
def update(id):
    t = Topic.one(id=id)
    if t is None:
        abort(404)
    else:
        files = request.files
        form = request.form

        data = json.loads(form['data'])
        process_content_data(data, files)
        # 更新编辑时间
        data['updated_time'] = time.time()

        Topic.update(id, **data)
        return make_response('编辑成功', 200)

