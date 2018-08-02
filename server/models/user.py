from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib

from models import SQLMixin, db

class User(SQLMixin, db.Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """
    __tablename__ = 'User'

    username = Column(String(50), nullable=False)
    password = Column(String(256), nullable=False)
    avatar = Column(String(100), nullable=False, default='/images/user_default.png')
    # 与话题关联
    topics = relationship('Topic')

    @classmethod
    def guest(cls):
        guest = {
            'username': '游客',
            'avatar': 'images/user_default.png',
            'is_guest': True,
        }
        return guest

    @classmethod
    def salted_password(cls, password, salt='$!@><?>HUI&DWQa`'):
        """加盐密码"""
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        print('sha256', len(hash2))
        return hash2

    def hashed_password(self, pwd):
        """摘要密码"""
        # 用 ascii 编码转换成 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        # 返回摘要字符串
        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        # 名字长度小于 2 或 名字已存在则不能注册
        if len(name) > 2 and User.one(username=name) is None:
            u = User.new(form)
            u.password = u.salted_password(pwd)
            u.save()
            return u
        else:
            return None

    @classmethod
    def validate_signin(cls, form):
        user = User.one(username=form['username'])
        if user is not None and user.password == User.salted_password(form['password']):
            return user
        else:
            return None
