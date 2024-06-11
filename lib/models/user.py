# lib/models/user.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Password should be hashed in a real application

    movies = relationship('Movie', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User(username={self.username})>"

    @classmethod
    def create(cls, session, username, password):
        user = cls(username=username, password=password)
        session.add(user)
        session.commit()
        return user

    @classmethod
    def find_by_username(cls, session, username):
        return session.query(cls).filter_by(username=username).one_or_none()
