'''
重置数据库
'''

from sqlalchemy import create_engine

import config
from app import configured_app
from models import db
from models.topic import Topic
from models.user import User
from models.board import Board


def reset_database():
    url = 'mysql+pymysql://root:{}@localhost/?charset=utf8mb4'.format(config.database_password)
    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS {}'.format(config.database))
        c.execute('CREATE DATABASE {} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'.format(config.database))
        c.execute('USE {}'.format(config.database))

    db.metadata.create_all(bind=e)


def generate_fake_data():
    with open('markdown_demo.md', encoding='utf-8') as f:
        content = f.read()

    guest_form = dict(
        username='游客',
        password=''
    )
    u_form = dict(
        username="phoe",
        password="1be6af03717a0906a774a129ac467fcea8f89849df003548a8039cffffb12baf"
    )

    User.new(guest_form)
    User.new(u_form)

    b = Board.new({
        'name': '全部',
    })

    for n in ['编程', '艺术']:
        Board.new({
            'name': n,
        })

    topic_form = dict(
        title='markdown demo',
        content=content,
    )

    Topic.new(topic_form, 2, b.id)


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_data()