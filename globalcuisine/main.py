# globalcuisine/main.py
from flask import Blueprint, abort, render_template
from .forms import CreateChallengeForm
from flask import flash

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

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

from .recipes import recipes  # Import the recipes list from the recipes module
@main.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    # Fetch recipe details from the database (currently in a dictionary in recipes.py)
    recipe = next((r for r in recipes if r['id'] == recipe_id), None)
    if recipe:
        return render_template('recipe.html', recipe=recipe)
    else:
        abort(404)
    
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

