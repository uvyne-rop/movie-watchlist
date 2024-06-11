import click
from helpers import SessionLocal, Movie, Review, Category
from models import Base
from sqlalchemy.exc import OperationalError

class MovieWatchlistCLI:
    def __init__(self):
        self.session = SessionLocal()
        self.database_initialized = False  # Flag to track if the database is initialized

    def display_menu(self):
        """Display the main menu."""
        click.echo("1. Initialize Database")
        click.echo("2. Movie Management")
        click.echo("3. Review Management")
        click.echo("4. Category Management")
        click.echo("5. Exit")

    def run(self):
        """Run the CLI application."""
        while True:
            self.display_menu()
            choice = click.prompt("Enter your choice", type=int)

            if choice == 1:
                self.initialize_database()
            elif choice == 2:
                if self.check_initialization():
                    self.movie_management()
            elif choice == 3:
                if self.check_initialization():
                    self.review_management()
            elif choice == 4:
                if self.check_initialization():
                    self.category_management()
            elif choice == 5:
                click.echo("Exiting...")
                break
            else:
                click.echo("Invalid choice. Please try again.")

    def initialize_database(self):
        """Initialize the database by creating all necessary tables."""
        click.echo("Initializing the database...")
        Base.metadata.create_all(self.session.bind)
        self.database_initialized = True
        click.echo("Database initialized successfully.")

    def check_initialization(self):
        """Check if the database is initialized."""
        if self.database_initialized:
            return True
        try:
            # Check if any table exists
            self.session.execute('SELECT 1 FROM movies LIMIT 1')
            self.database_initialized = True
            return True
        except OperationalError:
            click.echo("Database not initialized. Please initialize the database first.")
            return False

    def movie_management_menu(self):
        """Display the movie management menu."""
        click.echo("1. Add a new movie to the watchlist.")
        click.echo("2. Delete a movie from the watchlist by ID.")
        click.echo("3. List all movies in the watchlist.")
        click.echo("4. Show details for a specific movie by ID.")
        click.echo("5. List all movies in a specific category.")
        click.echo("6. Mark a movie as watched.")
        click.echo("7. Mark a movie as not watched.")
        click.echo("8. Return to main menu")

    def movie_management(self):
        """Handle movie management operations."""
        while True:
            self.movie_management_menu()
            choice = click.prompt("Enter your choice", type=int)

            if choice == 1:
                self.add_movie()
            elif choice == 2:
                self.delete_movie()
            elif choice == 3:
                self.list_movies()
            elif choice == 4:
                self.show_movie_details()
            elif choice == 5:
                self.list_movies_by_category()
            elif choice == 6:
                self.mark_movie_watched()
            elif choice == 7:
                self.mark_movie_not_watched()
            elif choice == 8:
                break
            else:
                click.echo("Invalid choice. Please try again.")

    def add_movie(self):
        """Add a new movie to the watchlist."""
        title = click.prompt("Enter the title of the movie")
        director = click.prompt("Enter the director of the movie")
        genre = click.prompt("Enter the genre of the movie")
        category_id = click.prompt("Enter the category ID for the movie (optional)", type=int, default=None)

        movie = Movie.create(self.session, title, director, genre, category_id)
        click.echo(f"Movie added: {movie}")

    def delete_movie(self):
        """Delete a movie from the watchlist by ID."""
        movie_id = click.prompt("Enter the ID of the movie to delete", type=int)
        success = Movie.delete(self.session, movie_id)
        if success:
            click.echo("Movie deleted successfully.")
        else:
            click.echo("Movie not found.")

    def list_movies(self):
        """List all movies in the watchlist with their IDs and watched status."""
        movies = Movie.get_all(self.session)
        if movies:
            click.echo("List of movies in the watchlist:")
            for movie in movies:
                watched_status = "Watched" if movie.watched else "Not Watched"
                click.echo(f"ID: {movie.id}, Title: {movie.title}, Director: {movie.director}, Genre: {movie.genre}, Watched: {watched_status}, Category ID: {movie.category_id}")
        else:
            click.echo("No movies found in the watchlist.")

    def show_movie_details(self):
        """Show details for a specific movie by ID."""
        movie_id = click.prompt("Enter the ID of the movie to show details", type=int)
        movie = Movie.find_by_id(self.session, movie_id)
        if movie:
            watched_status = "Watched" if movie.watched else "Not Watched"
            click.echo(f"ID: {movie.id}, Title: {movie.title}, Director: {movie.director}, Genre: {movie.genre}, Watched: {watched_status}, Category ID: {movie.category_id}")
        else:
            click.echo("Movie not found.")

    def list_movies_by_category(self):
        """List all movies in a specific category."""
        category_id = click.prompt("Enter the ID of the category to list movies", type=int)
        movies = Movie.find_by_category(self.session, category_id)
        if movies:
            click.echo(f"Movies in category {category_id}:")
            for movie in movies:
                watched_status = "Watched" if movie.watched else "Not Watched"
                click.echo(f"ID: {movie.id}, Title: {movie.title}, Watched: {watched_status}")
        else:
            click.echo("No movies found in this category.")

    def mark_movie_watched(self):
        """Mark a movie as watched."""
        movie_id = click.prompt("Enter the ID of the movie to mark as watched", type=int)
        movie = Movie.mark_watched(self.session, movie_id, watched=True)
        if movie:
            click.echo(f"Movie '{movie.title}' marked as watched.")
        else:
            click.echo("Movie not found.")

    def mark_movie_not_watched(self):
        """Mark a movie as not watched."""
        movie_id = click.prompt("Enter the ID of the movie to mark as not watched", type=int)
        movie = Movie.mark_watched(self.session, movie_id, watched=False)
        if movie:
            click.echo(f"Movie '{movie.title}' marked as not watched.")
        else:
            click.echo("Movie not found.")

    def review_management(self):
        """Handle review management operations."""
        while True:
            self.review_management_menu()
            choice = click.prompt("Enter your choice", type=int)

            if choice == 1:
                self.add_review()
            elif choice == 2:
                self.delete_review()
            elif choice == 3:
                break
            else:
                click.echo("Invalid choice. Please try again.")

    def review_management_menu(self):
        """Display the review management menu."""
        click.echo("1. Add a review to a movie.")
        click.echo("2. Delete a review by ID.")
        click.echo("3. Return to main menu")

    def add_review(self):
        """Add a review to a movie."""
        movie_id = click.prompt("Enter the ID of the movie to add a review", type=int)
        while True:
            try:
                rating = click.prompt("Enter the rating for the movie (1 to 5 stars)", type=float)
                if not (1 <= rating <= 5):
                    raise ValueError("Rating must be between 1 and 5 stars.")
                break  # If valid, exit the loop
            except ValueError as e:
                click.echo(str(e))
        
        comment = click.prompt("Enter your comment for the movie")

        try:
            review = Review.create(self.session, movie_id, rating, comment)
            click.echo(f"Review added: {review}")
        except Exception as e:
            click.echo(f"Failed to add review: {str(e)}")

    def delete_review(self):
        """Delete a review by ID."""
        review_id = click.prompt("Enter the ID of the review to delete", type=int)
        success = Review.delete(self.session, review_id)
        if success:
            click.echo("Review deleted successfully.")
        else:
            click.echo("Review not found.")

    def category_management(self):
        """Handle category management operations."""
        while True:
            self.category_management_menu()
            choice = click.prompt("Enter your choice", type=int)

            if choice == 1:
                self.list_categories()
            elif choice == 2:
                break
            else:
                click.echo("Invalid choice. Please try again.")

    def category_management_menu(self):
        """Display the category management menu."""
        click.echo("1. List all categories.")
        click.echo("2. Return to main menu")

    def list_categories(self):
        """List all categories."""
        categories = Category.get_all(self.session)
        for category in categories:
            click.echo(f"ID: {category.id}, Name: {category.name}")

if __name__ == '__main__':
    cli = MovieWatchlistCLI()
    cli.run()
