# lib/helpers.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from models.user import User
from models.movie import Movie
from models.category import Category
from models.review import Review

DATABASE_URL = "sqlite:///./Movie-Watchlist.db" 

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def initialize_database():
    Base.metadata.create_all(engine)
