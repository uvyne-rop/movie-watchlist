# cli.py
import click
from database import SessionLocal, init_db
from models import Movie, Review, Category
