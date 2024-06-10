import click
from models import SessionLocal, init_db
from helpers import Movie, Review, Category

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

@cli.command()
def list_movies():
    """List all movies in the watchlist."""
    session = SessionLocal()
    movies = Movie.get_all(session)
    for movie in movies:
        category = session.query(Category).filter_by(id=movie.category_id).one_or_none()
        category_name = category.name if category else "No Category"
        click.echo(f"{movie} - Category: {category_name}")

@cli.command()
@click.argument('movie_id', type=int)
def show_movie(movie_id):
    """Show details for a specific movie by ID."""
    session = SessionLocal()
    movie = Movie.find_by_id(session, movie_id)
    if movie:
        category = session.query(Category).filter_by(id=movie.category_id).one_or_none()
        category_name = category.name if category else "No Category"
        click.echo(f"{movie} - Category: {category_name}")
        for review in movie.reviews:
            click.echo(f"  Review: {review}")
    else:
        click.echo("Movie not found.")

@cli.command()
@click.argument('movie_id', type=int)
@click.argument('rating', type=float)
@click.argument('comment')
def add_review(movie_id, rating, comment):
    """Add a review to a movie."""
    session = SessionLocal()
    review = Review.create(session, movie_id, rating, comment)
    click.echo(f"Review added: {review}")

@cli.command()
@click.argument('review_id', type=int)
def delete_review(review_id):
    """Delete a review by ID."""
    session = SessionLocal()
    success = Review.delete(session, review_id)
    if success:
        click.echo("Review deleted successfully.")
    else:
        click.echo("Review not found.")

@cli.command()
def list_categories():
    """List all categories."""
    session = SessionLocal()
    categories = Category.get_all(session)
    for category in categories:
        click.echo(category)

@cli.command()
@click.argument('category_id', type=int)
def list_movies_by_category(category_id):
    """List all movies in a specific category."""
    session = SessionLocal()
    category = Category.find_by_id(session, category_id)
    if category:
        movies = Movie.find_by_category(session, category_id)
        click.echo(f"Movies in category '{category.name}':")
        for movie in movies:
            click.echo(movie)
    else:
        click.echo("Category not found.")

@cli.command()
def initdb():
    """Initialize the database."""
    init_db()
    click.echo("Database initialized.")

if __name__ == '__main__':
    cli()