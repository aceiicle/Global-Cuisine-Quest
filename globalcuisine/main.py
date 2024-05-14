# globalcuisine/main.py
from flask import Blueprint, abort, render_template, flash
from .forms import CreateChallengeForm
from .models import Recipe

main = Blueprint('main', __name__)

@main.route('/')
def index():
    recipes = Recipe.query.all()
    asian_recipes = Recipe.get_random_recipes('Asian', count=3)
    european_recipes = Recipe.get_random_recipes('European', count=3)
    australian_recipes = Recipe.get_random_recipes('Australian', count=3)
    south_american_recipes = Recipe.get_random_recipes('South American', count=3)
    north_american_recipes = Recipe.get_random_recipes('North American', count=3)
    african_recipes = Recipe.get_random_recipes('African', count=3)
    return render_template('index.html', recipes=recipes,
                            asian_recipes=asian_recipes, 
                            european_recipes=european_recipes,
                            australian_recipes=australian_recipes, 
                            south_american_recipes=south_american_recipes,
                            north_american_recipes=north_american_recipes, 
                            african_recipes=african_recipes)

@main.route('/dashboard')
def dashboard():
    # Add logic to fetch data for the dashboard here
    return render_template('dashboard.html')

@main.route('/challenges')
def challenge_list():
    # Fetch challenges from the database or define them
    challenges = []  # Replace with actual data fetching logic
    return render_template('challenge_list.html', challenges=challenges)


from flask import redirect  # Import the redirect function
from flask import url_for  # Import the url_for function

@main.route('/create-challenge', methods=['GET', 'POST'])
def create_challenge():
    form = CreateChallengeForm()
    if form.validate_on_submit():
        # Process form data
        flash('Challenge created successfully!', 'success')
        return redirect(url_for('main.challenge_list'))
    return render_template('create_challenge.html', form=form)


from .models import Recipe

@main.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    # Fetch recipe details from the database defined in models.py
    recipe = Recipe.query.get(recipe_id)
    if recipe:
        return render_template('recipe.html', recipe=recipe)
    else:
        abort(404)
    
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

