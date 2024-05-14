# globalcuisine/main.py
import os
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from . import db
from .models import User, Challenge, Submission, Recipe
from .forms import CreateChallengeForm, LoginForm, RegistrationForm

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

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route('/create_challenge', methods=['GET', 'POST'])
@login_required
def create_challenge():
    form = CreateChallengeForm()
    if form.validate_on_submit():
        # Extract file from form, if present
        image_file = form.image.data
        filename = None
        if image_file:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
        
        # Create new Challenge object including the image filename if available
        challenge = Challenge(
            title=form.title.data,
            recipe_type=form.recipe_type.data,
            description=form.description.data,
            is_recipe=form.is_recipe.data,
            ingredients=form.ingredients.data,
            recipe_instructions=form.recipe_instructions.data,
            cuisine_type=form.cuisine_type.data,
            cuisine_style=form.cuisine_style.data,
            difficulty_level=form.difficulty_level.data,
            image_filename=filename,  # Save filename to the database
            user_id=current_user.id
        )
        db.session.add(challenge)
        db.session.commit()
        flash('Your challenge has been created!', 'success')
        return redirect(url_for('main.challenge_list'))
    else:
        # If form doesn't validate, log errors
        print(form.errors)

    return render_template('create_challenge.html', title='Create Challenge', form=form)


@main.route('/view_challenges') # or it is challenges
def challenge_list():
    challenges = Challenge.query.all()
    return render_template('challenge_list.html', challenges=challenges)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

@main.route('/challenge/<int:challenge_id>')
def challenge_detail(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    return render_template('challenge_detail.html', challenge=challenge)
