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

from globalcuisine.models import Recipe

def add_initial_recipes():
    app = create_app()  # Create an instance of Flask app
    with app.app_context():  # Use the application context to access the database
        # Check if any data exists, and if not, add the recipes
        if Recipe.query.count() == 0:
            recipes = [
                Recipe(
                    name='Sushi',
                    image='sushi.png',
                    description='A traditional Japanese dish made with vinegared rice and seafood.',
                    region='Asian',
                    cuisine='Japanese',
                    ingredients='Rice, Nori, Fish, Vegetables',
                    preparation_time='30',
                    cooking_time='0',
                    steps='Cook the rice and let it cool. Prepare the fish and vegetables. Lay out the nori and rice. Add the fish and vegetables. Roll the sushi and cut into pieces.'
                ),
                Recipe(
                    name='Ramen',
                    image='ramen.png',
                    description='A noodle soup dish that originated in China and has been adapted in Japan.',
                    region='Asian',
                    cuisine='Japanese',
                    ingredients='Noodles, Broth, Meat, Vegetables',
                    preparation_time='15',
                    cooking_time='30',
                    steps='Prepare the broth and noodles. Cook the meat and vegetables. Add the noodles and broth. Serve hot.'
                ),
                Recipe(
                    name='Pad Thai',
                    image='pad-thai.png',
                    description='A popular Thai stir-fried noodle dish made with rice noodles, shrimp, and vegetables.',
                    region='Asian',
                    cuisine='Thai',
                    ingredients='Rice noodles, Shrimp, Tofu, Bean sprouts',
                    preparation_time='20',
                    cooking_time='15',
                    steps='Soak the noodles in warm water. Cook the shrimp and tofu. Add the noodles and bean sprouts. Stir-fry with the sauce and serve hot.'
                ),
                Recipe(
                    name='Mango Pancakes',
                    image='mango-pancakes.png',
                    description='Delicious pancakes with fresh mango slices and syrup.',
                    region='Asian',
                    cuisine='Filipino',
                    ingredients='Pancake mix, Mangoes, Syrup',
                    preparation_time='10',
                    cooking_time='15',
                    steps='Prepare the pancake batter. Cook the pancakes. Top with mango slices and syrup.'
                ),
                Recipe(
                    name='Thai Turmeric Chicken',
                    image='thai-turmeric-chicken.png',
                    description='A flavorful Thai dish made with turmeric-marinated chicken.',
                    region='Asian',
                    cuisine='Thai',
                    ingredients='Chicken, Turmeric, Lemongrass, Garlic',
                    preparation_time='30',
                    cooking_time='30',
                    steps='Marinate the chicken with turmeric and spices. Grill or bake until cooked through.'
                ),
                Recipe(
                    name='Bok Choy in Ginger Sauce',
                    image='bok-choy-ginger-sauce.png',
                    description='A simple and healthy dish made with bok choy and ginger sauce.',
                    region='Asian',
                    cuisine='Chinese',
                    ingredients='Bok choy, Ginger, Soy sauce, Garlic',
                    preparation_time='10',
                    cooking_time='10',
                    steps='Blanch the bok choy. Prepare the ginger sauce. Toss the bok choy in the sauce and serve.'
                ),
                Recipe(
                    name='Garlic Noodles',
                    image='garlic-noodles.png',
                    description='A flavorful noodle dish made with garlic and butter.',
                    region='Asian',
                    cuisine='Vietnamese',
                    ingredients='Noodles, Garlic, Butter, Soy sauce',
                    preparation_time='10',
                    cooking_time='15',
                    steps='Cook the noodles according to package instructions. In a pan, melt butter and sauté minced garlic until fragrant. Add cooked noodles and soy sauce, toss to coat. Serve hot.'
                ),
                Recipe(
                    name='Vegetable Dumplings',
                    image='vegetable-dumplings.png',
                    description='Delicious dumplings filled with a mixture of vegetables.',
                    region='Asian',
                    cuisine='Chinese',
                    ingredients='Dumpling wrappers, Cabbage, Carrots, Mushrooms, Green onions',
                    preparation_time='30',
                    cooking_time='15',
                    steps='Finely chop the cabbage, carrots, mushrooms, and green onions. Mix the vegetables together in a bowl. Place a spoonful of the vegetable mixture onto a dumpling wrapper. Fold the wrapper in half and seal the edges. Steam the dumplings for about 10 minutes or until cooked through. Serve hot with dipping sauce.'
                ),
                Recipe(
                    name='Pizza',
                    image='pizza.png',
                    description='A classic Italian dish made with a flatbread base and various toppings.',
                    region='European',
                    cuisine='Italian',
                    ingredients='Dough, Tomato sauce, Cheese, Toppings',
                    preparation_time='60',
                    cooking_time='15',
                    steps='Prepare the dough and tomato sauce. Add the cheese and toppings. Bake in the oven until crispy.'
                )
                # Add more recipes as necessary
            ]
            db.session.bulk_save_objects(recipes)
            db.session.commit()
            print("Recipes added to the database.")
        else:
            print("Database already initialized with recipes.")

if __name__ == '__main__':
    # add_initial_challenges()
    # drop the recipe table and recreate it
    add_initial_recipes()