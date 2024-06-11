# lib/models/movie.py

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from . import Base

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    director = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    watched = Column(Boolean, default=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    category = relationship('Category', back_populates='movies')
    reviews = relationship('Review', back_populates='movie', cascade='all, delete-orphan')
    user = relationship('User', back_populates='movies')

    def __repr__(self):
        return f"<Movie(title={self.title}, director={self.director}, genre={self.genre}, watched={self.watched})>"
    
    @classmethod
    def create(cls, session, title, director, genre, user_id, category_id=None):
        movie = cls(title=title, director=director, genre=genre, user_id=user_id, category_id=category_id)
        session.add(movie)
        session.commit()
        return movie

    @classmethod
    def delete(cls, session, movie_id):
        movie = session.query(cls).filter_by(id=movie_id).one_or_none()
        if movie:
            session.delete(movie)
            session.commit()
            return True
        return False
    
    @classmethod
    def get_all(cls, session, user_id):
        return session.query(cls).filter_by(user_id=user_id).all()

    @classmethod
    def find_by_id(cls, session, movie_id):
        return session.query(cls).filter_by(id=movie_id).one_or_none()

    @classmethod
    def find_by_category(cls, session, category_id, user_id):
        return session.query(cls).filter_by(category_id=category_id, user_id=user_id).all()

    @classmethod
    def mark_watched(cls, session, movie_id, watched):
        movie = cls.find_by_id(session, movie_id)
        if movie:
            movie.watched = watched
            session.commit()
            return movie
        return None
