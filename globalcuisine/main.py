# globalcuisine/main.py
import os
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from . import db
from .models import ActiveChallenge, User, Challenge, Submission, Recipe, CompletedChallenge
from .forms import CreateChallengeForm, LoginForm, RegistrationForm, SubmissionForm

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

    return render_template('create_challenge.html', title='Create Challenge', form=form)


@main.route('/challenge_list/', defaults={'sort_by': 'newest'})
@main.route('/view_challenges/<sort_by>') # or it is challenges
def challenge_list(sort_by):
    if sort_by == 'newest':
        challenges = Challenge.query.order_by(Challenge.created_at.desc()).all()
    elif sort_by == 'oldest':
        challenges = Challenge.query.order_by(Challenge.created_at.asc()).all()
    elif sort_by == 'difficulty':
        challenges = Challenge.query.order_by(Challenge.difficulty_level.desc()).all()
    else:
        challenges = Challenge.query.all() #Default no sorting
    return render_template('challenge_list.html', challenges=challenges)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/dashboard')
@login_required
def dashboard():
    active_challenges = ActiveChallenge.query.filter_by(user_id=current_user.id).all()
    completed_challenges = CompletedChallenge.query.filter_by(user_id=current_user.id).all()
    suggested_challenges = Challenge.query.filter(~Challenge.id.in_(
        [ac.challenge_id for ac in active_challenges] + [cc.challenge_id for cc in completed_challenges])).all()

    return render_template('dashboard.html', title='Dashboard', 
                           active_challenges=active_challenges, 
                           completed_challenges=completed_challenges, 
                           suggested_challenges=suggested_challenges)



@main.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    # Fetch recipe details from the database defined in models.py
    recipe = Recipe.query.get(recipe_id)
    if recipe:
        return render_template('recipe.html', recipe=recipe)
    else:
        abort(404)

@main.route('/challenge/<int:challenge_id>')
@login_required
def challenge_detail(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    active_challenge = ActiveChallenge.query.filter_by(user_id=current_user.id, challenge_id=challenge_id).first()
    completed_challenge = CompletedChallenge.query.filter_by(user_id=current_user.id, challenge_id=challenge_id).first()
    submissions = Submission.query.filter_by(challenge_id=challenge_id).all()
    return render_template('challenge_detail.html', challenge=challenge, active_challenge=active_challenge,
                           completed_challenge=completed_challenge, submissions=submissions)




@main.route('/challenge/<int:challenge_id>/submit', methods=['GET', 'POST'])
@login_required
def submit_challenge(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    active_challenge = ActiveChallenge.query.filter_by(user_id=current_user.id, challenge_id=challenge_id).first()

    if not active_challenge:
        flash('You have not accepted this challenge.', 'danger')
        return redirect(url_for('main.challenge_detail', challenge_id=challenge_id))

    form = SubmissionForm()
    if form.validate_on_submit():
        submission = Submission(comment=form.comment.data, user_id=current_user.id, challenge_id=challenge_id)
        db.session.add(submission)
        
        # Remove from active challenges
        db.session.delete(active_challenge)
        
        # Add to completed challenges
        completed_challenge = CompletedChallenge(user_id=current_user.id, challenge_id=challenge_id)
        db.session.add(completed_challenge)
        db.session.commit()

        flash('You have successfully submitted the challenge.', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('submit_challenge.html', challenge=challenge, form=form)

@main.route('/challenge/<int:challenge_id>/accept', methods=['POST'])
@login_required
def accept_challenge(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    active_challenge = ActiveChallenge.query.filter_by(user_id=current_user.id, challenge_id=challenge_id).first()

    if active_challenge is None:
        active_challenge = ActiveChallenge(user_id=current_user.id, challenge_id=challenge_id)
        db.session.add(active_challenge)
        db.session.commit()
        flash('You have accepted the challenge!', 'success')
    else:
        flash('You have already accepted this challenge!', 'warning')

    return redirect(url_for('main.challenge_detail', challenge_id=challenge_id))

@main.route('/challenge/<int:challenge_id>/cancel', methods=['POST'])
@login_required
def cancel_challenge(challenge_id):
    active_challenge = ActiveChallenge.query.filter_by(user_id=current_user.id, challenge_id=challenge_id).first()
    if active_challenge:
        db.session.delete(active_challenge)
        db.session.commit()
        flash('You have successfully canceled the challenge.', 'success')
    else:
        flash('You have not accepted this challenge.', 'danger')
    return redirect(url_for('main.dashboard'))



@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404