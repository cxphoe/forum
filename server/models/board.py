from sqlalchemy import Column, Unicode
from sqlalchemy.orm import relationship

from models import SQLMixin, db

class Board(SQLMixin, db.Model):
    __tablename__ = 'Board'

    name = Column(Unicode(50), nullable=False)
    topics = relationship('Topic')

