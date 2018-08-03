from sqlalchemy import Integer, Column, UnicodeText, ForeignKey

from models import SQLMixin, db

class Follow(SQLMixin, db.Model):
    __tablename__ = 'Follow'

    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    follower_id = Column(Integer, ForeignKey('User.id'), nullable=False)

