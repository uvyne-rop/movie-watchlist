# lib/models/category.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    movies = relationship('Movie', back_populates='category')

    def __repr__(self):
        return f"<Category(name={self.name})>"

    @classmethod
    def create(cls, session, name):
        category = cls(name=name)
        session.add(category)
        session.commit()
        return category

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, category_id):
        return session.query(cls).filter_by(id=category_id).one_or_none()

    @classmethod
    def delete(cls, session, category_id):
        category = cls.find_by_id(session, category_id)
        if category:
            session.delete(category)
            session.commit()
            return True
        return False
