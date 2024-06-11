# lib/models/review.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    rating = Column(Float, nullable=False)
    comment = Column(String, nullable=True)

    movie = relationship('Movie', back_populates='reviews')

    def __repr__(self):
        return f"<Review(movie_id={self.movie_id}, rating={self.rating}, comment={self.comment})>"

    @classmethod
    def create(cls, session, movie_id, rating, comment=None):
        review = cls(movie_id=movie_id, rating=rating, comment=comment)
        session.add(review)
        session.commit()
        return review

    @classmethod
    def find_by_id(cls, session, review_id):
        return session.query(cls).filter_by(id=review_id).one_or_none()

    @classmethod
    def delete(cls, session, review_id):
        review = cls.find_by_id(session, review_id)
        if review:
            session.delete(review)
            session.commit()
            return True
        return False

    @classmethod
    def get_reviews_for_movie(cls, session, movie_id):
        return session.query(cls).filter_by(movie_id=movie_id).all()
