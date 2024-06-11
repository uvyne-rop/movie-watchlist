# lib/cli.py

import click
from helpers import SessionLocal, initialize_database
from models.user import User
from models.movie import Movie
from models.review import Review
from models.category import Category

class MovieWatchlistCLI:
    def __init__(self):
        self.session = SessionLocal()
        self.database_initialized = False
        self.current_user = None

    def display_menu(self):
        """Display the main menu."""
        click.echo("1. Initialize Database")
        click.echo("2. Register")
        click.echo("3. Login")
        click.echo("4. Movie Management")
        click.echo("5. Review Management")
        click.echo("6. Category Management")
        click.echo("7. Logout")
        click.echo("8. Exit")

    def run(self):
        """Run the CLI application."""
        while True:
            self.display_menu()
            choice = click.prompt("Enter your choice", type=int)

            if choice == 1:
                self.initialize_database()
            elif choice == 2:
                self.register()
            elif choice == 3:
                self.login()
            elif choice == 4:
                if self.check_user_login():
                    self.movie_management()
            elif choice == 5:
                if self.check_user_login():
                    self.review_management()
            elif choice == 6:
                if self.check_user_login():
                    self.category_management()
            elif choice == 7:
                self.logout()
            elif choice == 8:
                click.echo("Exiting...")
                break
            else:
                click.echo("Invalid choice. Please try again.")

    def initialize_database(self):
        """Initialize the database by creating all necessary tables."""
        click.echo("Initializing the database...")
        initialize_database()
        self.database_initialized = True
        click.echo("Database initialized successfully.")

    def register(self):
        """Register a new user."""
        username = click.prompt("Enter a username")
        password = click.prompt("Enter a password", hide_input=False, confirmation_prompt=True)

        if User.find_by_username(self.session, username):
            click.echo("Username already exists. Please choose a different username.")
        else:
            user = User.create(self.session, username, password)
            click.echo(f"User registered successfully: {user}")

    def login(self):
        """Login an existing user."""
        username = click.prompt("Enter your username")
        password = click.prompt("Enter your password", hide_input=True)

        user = User.find_by_username(self.session, username)
        if user and user.password == password:  # In a real app, check the hashed password
            self.current_user = user
            click.echo(f"Login successful. Welcome, {user.username}!")
        else:
            click.echo("Invalid username or password. Please try again.")

    def logout(self):
        """Logout the current user."""
        if self.current_user:
            click.echo(f"Goodbye, {self.current_user.username}!")
            self.current_user = None
        else:
            click.echo("No user is currently logged in.")

    def check_user_login(self):
        """Check if a user is logged in."""
        if self.current_user:
            return True
        else:
            click.echo("You need to login first.")
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
        category_id = click.prompt("Enter the category ID for the movie (optional)", type=int)

        if self.current_user:
            movie = Movie.create(self.session, title, director, genre, self.current_user.id, category_id)
            click.echo(f"Movie added: {movie}")
        else:
            click.echo("You need to login first.")

    def delete_movie(self):
        """Delete a movie from the watchlist by ID."""
        movie_id = click.prompt("Enter the ID of the movie to delete", type=int)
        if self.current_user:
            movie = Movie.find_by_id(self.session, movie_id)
            if movie and movie.user_id == self.current_user.id:
                success = Movie.delete(self.session, movie_id)
                if success:
                    click.echo("Movie deleted successfully.")
                else:
                    click.echo("Movie not found.")
            else:
                click.echo("You don't have permission to delete this movie.")
        else:
            click.echo("You need to login first.")

    def list_movies(self):
        """List all movies in the watchlist for the current user."""
        if self.current_user:
            movies = Movie.get_all(self.session, self.current_user.id)
            if movies:
                click.echo("List of movies in your watchlist:")
                for movie in movies:
                    watched_status = "Watched" if movie.watched else "Not Watched"
                    click.echo(f"ID: {movie.id}, Title: {movie.title}, Director: {movie.director}, Genre: {movie.genre}, Watched: {watched_status}, Category ID: {movie.category_id}")
            else:
                click.echo("No movies found in your watchlist.")
        else:
            click.echo("You need to login first.")

    def show_movie_details(self):
        """Show details for a specific movie by ID."""
        movie_id = click.prompt("Enter the ID of the movie to show details", type=int)
        if self.current_user:
            movie = Movie.find_by_id(self.session, movie_id)
            if movie and movie.user_id == self.current_user.id:
                watched_status = "Watched" if movie.watched else "Not Watched"
                click.echo(f"ID: {movie.id}, Title: {movie.title}, Director: {movie.director}, Genre: {movie.genre}, Watched: {watched_status}, Category ID: {movie.category_id}")
            else:
                click.echo("Movie not found or you don't have permission to view this movie.")
        else:
            click.echo("You need to login first.")

    def list_movies_by_category(self):
        """List all movies in a specific category for the current user."""
        category_id = click.prompt("Enter the ID of the category to list movies", type=int)
        if self.current_user:
            movies = Movie.find_by_category(self.session, category_id, self.current_user.id)
            if movies:
                click.echo(f"Movies in category {category_id}:")
                for movie in movies:
                    watched_status = "Watched" if movie.watched else "Not Watched"
                    click.echo(f"ID: {movie.id}, Title: {movie.title}, Watched: {watched_status}")
            else:
                click.echo("No movies found in this category.")
        else:
            click.echo("You need to login first.")

    def mark_movie_watched(self):
        """Mark a movie as watched."""
        movie_id = click.prompt("Enter the ID of the movie to mark as watched", type=int)
        if self.current_user:
            movie = Movie.mark_watched(self.session, movie_id, watched=True)
            if movie and movie.user_id == self.current_user.id:
                click.echo(f"Movie '{movie.title}' marked as watched.")
            else:
                click.echo("Movie not found or you don't have permission to mark this movie.")
        else:
            click.echo("You need to login first.")

    def mark_movie_not_watched(self):
        """Mark a movie as not watched."""
        movie_id = click.prompt("Enter the ID of the movie to mark as not watched", type=int)
        if self.current_user:
            movie = Movie.mark_watched(self.session, movie_id, watched=False)
            if movie and movie.user_id == self.current_user.id:
                click.echo(f"Movie '{movie.title}' marked as not watched.")
            else:
                click.echo("Movie not found or you don't have permission to mark this movie.")
        else:
            click.echo("You need to login first.")

    def review_management_menu(self):
        """Display the review management menu."""
        click.echo("1. Add a review to a movie.")
        click.echo("2. Delete a review by ID.")
        click.echo("3. Return to main menu")

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

    def add_review(self):
        """Add a review to a movie."""
        movie_id = click.prompt("Enter the ID of the movie to add a review", type=int)
        if self.current_user:
            movie = Movie.find_by_id(self.session, movie_id)
            if movie and movie.user_id == self.current_user.id:
                while True:
                    try:
                        rating = click.prompt("Enter the rating for the movie (1 to 5 stars)", type=float)
                        if not (1 <= rating <= 5):
                            raise ValueError("Rating must be between 1 and 5 stars.")
                        break
                    except ValueError as e:
                        click.echo(str(e))
                
                comment = click.prompt("Enter your comment for the movie")
                
                try:
                    review = Review.create(self.session, movie_id, rating, comment)
                    click.echo(f"Review added: {review}")
                except Exception as e:
                    click.echo(f"Failed to add review: {str(e)}")
            else:
                click.echo("Movie not found or you don't have permission to review this movie.")
        else:
            click.echo("You need to login first.")

    def delete_review(self):
        """Delete a review by ID."""
        review_id = click.prompt("Enter the ID of the review to delete", type=int)
        if self.current_user:
            review = Review.find_by_id(self.session, review_id)
            if review and review.movie.user_id == self.current_user.id:
                success = Review.delete(self.session, review_id)
                if success:
                    click.echo("Review deleted successfully.")
                else:
                    click.echo("Review not found.")
            else:
                click.echo("You don't have permission to delete this review.")
        else:
            click.echo("You need to login first.")

    def category_management_menu(self):
        """Display the category management menu."""
        click.echo("1. List all categories.")
        click.echo("2. Return to main menu")

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

    def list_categories(self):
        """List all categories."""
        categories = Category.get_all(self.session)
        for category in categories:
            click.echo(f"ID: {category.id}, Name: {category.name}")

if __name__ == '__main__':
    cli = MovieWatchlistCLI()
    cli.run()
