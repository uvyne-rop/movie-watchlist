# cli.py
import click
from database import SessionLocal, init_db
from models import Movie, Review, Category

@click.group()
def cli():
    """Movie Watchlist CLI"""
    pass

@cli.command()
@click.argument('title')
@click.argument('director')
@click.argument('genre')
@click.option('--category', default=None, help="Category ID for the movie")

def add_movie(title, director, genre, category):
    """Add a new movie to the watchlist."""
    session = SessionLocal()
    movie = Movie.create(session, title, director, genre, category)
    click.echo(f"Movie added: {movie}")

@cli.command()
@click.argument('movie_id', type=int)
def delete_movie(movie_id):
    """Delete a movie from the watchlist by ID."""
    session = SessionLocal()
    success = Movie.delete(session, movie_id)
    if success:
        click.echo("Movie deleted successfully.")
    else:
        click.echo("Movie not found.")