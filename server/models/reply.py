from sqlalchemy import Integer, Column, UnicodeText, ForeignKey

from models import SQLMixin, db

class Reply(SQLMixin, db.Model):
    __tablename__ = 'Reply'

    content = Column(UnicodeText, nullable=False)
    topic_id = Column(Integer, ForeignKey('Topic.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    target_id = Column(Integer, ForeignKey('User.id'))

