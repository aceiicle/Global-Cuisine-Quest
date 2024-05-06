from globalcuisine import create_app, db  # Import the Flask application creation function and the database instance
from globalcuisine.models import Challenge  # Import the Challenge model

def add_initial_challenges():
    app = create_app()  # Create an instance of Flask app
    with app.app_context():  # Use the application context to access the database
        # Check if any data exists, and if not, add the challenges
        if Challenge.query.count() == 0:
            challenges = [
                Challenge(
                    title='Italian Pasta Challenge',
                    description='Create an authentic Italian pasta dish.',
                    image_filename='italian_pasta.jpg'
                ),
                Challenge(
                    title='Chocolate Chip Cookie Bake-off',
                    description='Bake your best batch of chocolate chip cookies.',
                    image_filename='choc_chip_cookies.jpg'
                )
                # Add more challenges as necessary
            ]
            db.session.bulk_save_objects(challenges)
            db.session.commit()
            print("Challenges added to the database.")
        else:
            print("Database already initialized with challenges.")

if __name__ == '__main__':
    add_initial_challenges()
