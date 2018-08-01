import time

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

from utils import log

db = SQLAlchemy()

class SQLMixin(object):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_time = Column(Integer, default=time.time)
    updated_time = Column(Integer, default=time.time)

    @classmethod
    def new(cls, form):
        m = cls()
        for name, value in form.items():
            setattr(m, name, value)

        db.session.add(m)
        db.session.commit()

        return m

    @classmethod
    def delete(cls, id):
        m = cls.one(id=id)

        db.session.delete(m)
        db.session.commit()

    @classmethod
    def update(cls, id, **kwargs):
        # u.username = 'test'
        # db.session.add(u)
        # db.session.commit()
        m = cls.query.filter_by(id=id).first()
        for name, value in kwargs.items():
            setattr(m, name, value)

        db.session.add(m)
        db.session.commit()

    @classmethod
    def all(cls, **kwargs):
        ms = cls.query.filter_by(**kwargs).all()
        return ms

    @classmethod
    def one(cls, **kwargs):
        ms = cls.query.filter_by(**kwargs).first()
        return ms

    @classmethod
    def columns(cls):
        return cls.__mapper__.c.items()

    def __repr__(self):
        name = self.__class__.__name__
        s = ''
        for attr, column in self.columns():
            if hasattr(self, attr):
                v = getattr(self, attr)
                s += '{}: ({})\n'.format(attr, v)
        return '< {}\n{} >\n'.format(name, s)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        d = {}
        for column, _ in self.columns():
            d[column] = getattr(self, column)
        return d

    @classmethod
    def all_json(cls):
        ds = cls.all()
        return [d.json() for d in ds]
