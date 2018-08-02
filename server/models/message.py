from sqlalchemy import Integer, Column, UnicodeText, ForeignKey, Boolean

from models import SQLMixin, db

class Message(SQLMixin, db.Model):
    __tablename__ = 'Message'

    title = Column(UnicodeText, nullable=False)
    reply_id = Column(Integer, ForeignKey('Reply.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    read = Column(Boolean, default=False, nullable=False)

