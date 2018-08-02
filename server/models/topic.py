from sqlalchemy import String, Integer, Column, Text, UnicodeText, Unicode, ForeignKey
from sqlalchemy.orm import relationship

from models import SQLMixin, db

class Topic(SQLMixin, db.Model):
    __tablename__ = 'Topic'

    views = Column(Integer, nullable=False, default=0)
    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    # 与回复关联
    replys = relationship('Reply')

    @classmethod
    def new(cls, form, user_id):
        form['user_id'] = user_id
        m = super().new(form)
        return m


    @classmethod
    def get(cls, id):
        m = cls.one(id=id)
        m.views += 1
        m.save()
        return m

    def reply_count(self):
        count = len(self.replies())
        return count

    def last_update_user(self):
        rs = self.replies()
        if len(rs) > 0:
            rs.sort(lambda r1, r2: r1.updated_time - r2.updated_time)
            return rs[-1].user()
        else:
            return self.user()

