from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship, declarative_base
from database import Base, SessionLocal

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    movies = relationship('Movie', back_populates='category', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Category(name={self.name})>"

    @classmethod
    def create(cls, session, name):
        category = cls(name=name)
        session.add(category)
        session.commit()
        return category

    @classmethod
    def delete(cls, session, category_id):
        category = session.query(cls).filter_by(id=category_id).one_or_none()
        if category:
            session.delete(category)
            session.commit()
            return True
        return False

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, category_id):
        return session.query(cls).filter_by(id=category_id).one_or_none()

    @classmethod
    def find_by_name(cls, session, name):
        return session.query(cls).filter_by(name=name).one_or_none()
    
class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    director = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    watched = Column(Boolean, default=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    category = relationship('Category', back_populates='movies')
    reviews = relationship('Review', back_populates='movie', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Movie(title={self.title}, director={self.director}, genre={self.genre}, watched={self.watched})>"
    
    @classmethod
    def create(cls, session, title, director, genre, category_id=None):
        movie = cls(title=title, director=director, genre=genre, category_id=category_id)
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
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, movie_id):
        return session.query(cls).filter_by(id=movie_id).one_or_none()

    @classmethod
    def find_by_category(cls, session, category_id):
        return session.query(cls).filter_by(category_id=category_id).all()
class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Float, nullable=False)
    comment = Column(String, nullable=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    movie = relationship('Movie', back_populates='reviews')  

    def __repr__(self):
        return f"<Review(rating={self.rating}, comment={self.comment}, movie_id={self.movie_id})>"

    @classmethod
    def create(cls, session, movie_id, rating, comment):
        review = cls(movie_id=movie_id, rating=rating, comment=comment)
        session.add(review)
        session.commit()
        return review
    
    @classmethod
    def delete(cls, session, review_id):
        review = session.query(cls).filter_by(id=review_id).one_or_none()
        if review:
            session.delete(review)
            session.commit()
            return True
        return False
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, review_id):
        return session.query(cls).filter_by(id=review_id).one_or_none()