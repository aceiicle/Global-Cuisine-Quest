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
                ),
                Recipe(
                    name='Beef Tagine',
                    image='beef-tagine.png',
                    description='A North African slow-cooked stew braised at low temperatures.',
                    region='African',
                    cuisine='Moroccan',
                    ingredients='Beef, Onions, Carrots, Spices',
                    preparation_time='20',
                    cooking_time='120',
                    steps='Brown the beef. Add onions, carrots, and spices. Slow cook for 2 hours.'
                ),
                Recipe(
                    name='Brigadeiros',
                    image='brigadeiros.png',
                    description='A popular Brazilian chocolate truffle made with condensed milk, cocoa powder, and butter.',
                    region='South American',
                    cuisine='Brazilian',
                    ingredients='Condensed milk, Cocoa powder, Butter, Chocolate sprinkles',
                    preparation_time='10',
                    cooking_time='10',
                    steps='Cook condensed milk, cocoa powder, and butter until thickened. Let cool, shape into balls, and roll in chocolate sprinkles.'
                ),
                Recipe(
                    name='Buffalo Wings',
                    image='buffalo-wings.png',
                    description='Spicy chicken wings coated in a tangy sauce.',
                    region='North American',
                    cuisine='American',
                    ingredients='Chicken wings, Hot sauce, Butter, Vinegar',
                    preparation_time='10',
                    cooking_time='20',
                    steps='Fry the chicken wings. In a separate pan, melt butter and mix with hot sauce and vinegar. Toss wings in the sauce.'
                ),
                Recipe(
                    name='Ceviche',
                    image='ceviche.png',
                    description='A seafood dish made from fresh raw fish cured in citrus juices.',
                    region='South American',
                    cuisine='Peruvian',
                    ingredients='Fish, Lime, Onion, Cilantro',
                    preparation_time='20',
                    cooking_time='0',
                    steps='Chop the fish and marinate in lime juice. Add onions and cilantro. Serve chilled.'
                ),
                Recipe(
                    name='Chakalaka',
                    image='chakalaka.png',
                    description='A South African vegetable relish served with bread, pap, or curries.',
                    region='African',
                    cuisine='South African',
                    ingredients='Tomatoes, Beans, Peppers, Spices',
                    preparation_time='15',
                    cooking_time='30',
                    steps='Chop the vegetables and sauté with spices. Cook until tender.'
                ),
                Recipe(
                    name='Cheese Burger',
                    image='cheese-burger.png',
                    description='A sandwich consisting of a cooked patty of ground meat, usually beef, placed inside a sliced bread roll or bun.',
                    region='North American',
                    cuisine='American',
                    ingredients='Beef patty, Cheese, Bun, Lettuce, Tomato, Pickles',
                    preparation_time='10',
                    cooking_time='10',
                    steps='Cook the beef patty. Assemble the burger with cheese, bun, and toppings.'
                ),
                Recipe(
                    name='Chocolate Chip Cookies',
                    image='choc-chip-cookie.png',
                    description='Classic American cookies with chocolate chips.',
                    region='North American',
                    cuisine='American',
                    ingredients='Flour, Butter, Sugar, Chocolate chips',
                    preparation_time='15',
                    cooking_time='10',
                    steps='Mix the dough and fold in chocolate chips. Bake until golden brown.'
                ),
                Recipe(
                    name='Croissants',
                    image='croissants.png',
                    description='A buttery, flaky, and delicious French pastry.',
                    region='European',
                    cuisine='French',
                    ingredients='Flour, Butter, Yeast, Sugar',
                    preparation_time='180',
                    cooking_time='20',
                    steps='Prepare the dough and fold with butter. Shape and let rise. Bake until golden brown.'
                ),
                Recipe(
                    name='Empanadas',
                    image='empanadas.png',
                    description='A type of baked or fried turnover consisting of pastry and filling, common in Spanish and Latin American cultures.',
                    region='South American',
                    cuisine='Argentinian',
                    ingredients='Dough, Beef, Onions, Spices',
                    preparation_time='30',
                    cooking_time='20',
                    steps='Prepare the dough and filling. Assemble the empanadas and bake until golden brown.'
                ),
                Recipe(
                    name='Fish and Chips',
                    image='fish-n-chips.png',
                    description='A popular British dish of fried fish and potatoes.',
                    region='European',
                    cuisine='British',
                    ingredients='Fish, Potatoes, Batter, Oil',
                    preparation_time='20',
                    cooking_time='15',
                    steps='Prepare the batter and coat the fish. Fry the fish and chips until golden brown.'
                ),
                Recipe(
                    name='Lamington',
                    image='lamington.png',
                    description='An Australian dessert of sponge cake dipped in chocolate and coated with coconut.',
                    region='Australian',
                    cuisine='Australian',
                    ingredients='Sponge cake, Chocolate, Coconut',
                    preparation_time='30',
                    cooking_time='20',
                    steps='Bake the sponge cake. Dip in chocolate and coat with coconut.'
                ),
                Recipe(
                    name='Meat Pie',
                    image='meat-pie.png',
                    description='A savory pie filled with meat and other ingredients.',
                    region='Australian',
                    cuisine='Australian',
                    ingredients='Pie crust, Beef, Onions, Gravy',
                    preparation_time='30',
                    cooking_time='40',
                    steps='Prepare the filling and crust. Assemble the pie and bake until golden brown.'
                ),
                Recipe(
                    name='Meringues',
                    image='meringues.png',
                    description='Light, airy, and sweet cookies made from whipped egg whites and sugar.',
                    region='European',
                    cuisine='French',
                    ingredients='Egg whites, Sugar, Vanilla',
                    preparation_time='15',
                    cooking_time='60',
                    steps='Whip the egg whites and sugar until stiff peaks form. Bake at a low temperature until dry and crisp.'
                ),
                Recipe(
                    name='Pavlova',
                    image='pavlova.png',
                    description='A meringue-based dessert named after the Russian ballerina Anna Pavlova.',
                    region='Australian',
                    cuisine='Australian',
                    ingredients='Egg whites, Sugar, Cornstarch, Vinegar, Fruit',
                    preparation_time='20',
                    cooking_time='60',
                    steps='Whip the egg whites and sugar until stiff. Bake the meringue. Top with fruit and serve.'
                ),
                Recipe(
                    name='Peri Peri Chicken',
                    image='peri-peri-chicken.png',
                    description='A spicy African chicken dish marinated in peri-peri sauce.',
                    region='African',
                    cuisine='Mozambican',
                    ingredients='Chicken, Peri-peri sauce, Garlic, Lemon',
                    preparation_time='20',
                    cooking_time='40',
                    steps='Marinate the chicken in peri-peri sauce. Grill or bake until cooked through.'
                ),
                Recipe(
                    name='Poutine',
                    image='poutine.png',
                    description='A Canadian dish consisting of fries topped with cheese curds and gravy.',
                    region='North American',
                    cuisine='Canadian',
                    ingredients='Fries, Cheese curds, Gravy',
                    preparation_time='10',
                    cooking_time='20',
                    steps='Prepare the fries and gravy. Assemble the poutine with cheese curds and hot gravy.'
                ),
                Recipe(
                    name='Shortbread',
                    image='shortbread.png',
                    description='A classic Scottish biscuit made from sugar, butter, and flour.',
                    region='European',
                    cuisine='Scottish',
                    ingredients='Flour, Butter, Sugar',
                    preparation_time='10',
                    cooking_time='30',
                    steps='Mix the dough and shape. Bake until golden brown.'
                )
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