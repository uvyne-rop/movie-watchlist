import click
from helpers import SessionLocal, Movie, Review, Category

class MovieWatchlistCLI:
    def __init__(self):
        self.session = SessionLocal()

    def display_menu(self):
        """Display the menu."""
        click.echo("1. Movie Management")
        click.echo("2. Review Management")
        click.echo("3. Category Management")
        click.echo("4. Exit")

    def movie_management_menu(self):
        """Display the movie management menu."""
        click.echo("1. Add a new movie to the watchlist.")
        click.echo("2. Delete a movie from the watchlist by ID.")
        click.echo("3. List all movies in the watchlist.")
        click.echo("4. Show details for a specific movie by ID.")
        click.echo("5. List all movies in a specific category.")
        click.echo("6. Return to main menu")

    def review_management_menu(self):
        """Display the review management menu."""
        click.echo("1. Add a review to a movie.")
        click.echo("2. Delete a review by ID.")
        click.echo("3. Return to main menu")

    def category_management_menu(self):
        """Display the category management menu."""
        click.echo("1. List all categories.")
        click.echo("2. Return to main menu")

    def run(self):
        """Run the CLI application."""
        while True:
            self.display_menu()
            choice = click.prompt("Enter your choice", type=int)

            if choice == 1:
                self.movie_management()
            elif choice == 2:
                self.review_management()
            elif choice == 3:
                self.category_management()
            elif choice == 4:
                click.echo("Exiting...")
                break
            else:
                click.echo("Invalid choice. Please try again.")

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
                break
            else:
                click.echo("Invalid choice. Please try again.")

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

    def add_movie(self):
        """Add a new movie to the watchlist."""
        title = click.prompt("Enter the title of the movie")
        director = click.prompt("Enter the director of the movie")
        genre = click.prompt("Enter the genre of the movie")
        category_id = click.prompt("Enter the category ID for the movie (optional)", default=None)
        
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
        """List all movies in the watchlist."""
        movies = Movie.get_all(self.session)
        for movie in movies:
            click.echo(movie)

    def show_movie_details(self):
        """Show details for a specific movie by ID."""
        movie_id = click.prompt("Enter the ID of the movie to show details", type=int)
        movie = Movie.find_by_id(self.session, movie_id)
        if movie:
            click.echo(movie)
        else:
            click.echo("Movie not found.")

    def list_movies_by_category(self):
        """List all movies in a specific category."""
        category_id = click.prompt("Enter the ID of the category to list movies", type=int)
        movies = Movie.find_by_category(self.session, category_id)
        for movie in movies:
            click.echo(movie)

    def add_review(self):
        """Add a review to a movie."""
        movie_id = click.prompt("Enter the ID of the movie to add a review", type=int)
        rating = click.prompt("Enter the rating for the movie", type=float)
        comment = click.prompt("Enter your comment for the movie")
        
        review = Review.create(self.session, movie_id, rating, comment)
        click.echo(f"Review added: {review}")

    def delete_review(self):
        """Delete a review by ID."""
        review_id = click.prompt("Enter the ID of the review to delete", type=int)
        success = Review.delete(self.session, review_id)
        if success:
            click.echo("Review deleted successfully.")
        else:
            click.echo("Review not found.")

    def list_categories(self):
        """List all categories."""
        categories = Category.get_all(self.session)
        for category in categories:
            click.echo(category)

if __name__ == '__main__':
    cli = MovieWatchlistCLI()
    cli.run()
