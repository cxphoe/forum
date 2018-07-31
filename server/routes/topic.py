import os, uuid, json
from flask import (
    Blueprint,
    jsonify,
    redirect,
    request,
    url_for,
)

from models.topic import Topic
from utils import log

main = Blueprint('server_topic', __name__)


@main.route('/')
def index():
    return jsonify(Topic.all_json())


@main.route('/<int:id>')
def detail(id):
    log(id)
    t = Topic.get(id)
    log(t)
    return jsonify(t.json())


def processImg(file):
    # ../../root/.ssh/authorized_keys
    # filename = secure_filename(file.filename)
    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('images', filename)
    file.save(path)

    return '<img src="/images/{}">'.format(filename)


@main.route('/add', methods=['POST'])
def add():
    """ 接受到的是一个特殊的数据结构：
    request.files 接受到的是文章内容中上传的图片(图片名和文件的键值对)
    request.form['data']['content'] 接受到的数据是一个数组，成员的结构可能是：
        { 'type': 'text', 'data': 文本值 }
        { 'type': 'img', 'name': 文件名字（用于在 request.files 中查找文件）, 'data': 图片src }
    """
    files = request.files

    get_content = {
        'text': lambda item: item['data'],
        'image': lambda item: processImg(files[item['name']]),
    }

    data = json.loads(request.form['data'])
    log(files, data['content'])
    content_parts = []
    for item in data['content']:
        content_parts.append(get_content[item['type']](item))
    data['content'] = '\n'.join(content_parts)

    t = Topic.new(data)
    t.save()

    return ''

