from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, Challenge, Submission
from .forms import CreateChallengeForm, LoginForm, RegistrationForm
from . import create_app

app = create_app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and check_password_hash(user.password_hash, form.password.data):
#             login_user(user, remember=form.remember.data)

#             next_page = request.args.get('next')
#             return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
#         else:
#             flash('Login Unsuccessful. Please check email and password', 'danger')
#     return render_template('login.html', title='Login', form=form)

@app.route('/create_challenge', methods=['GET', 'POST'])
@login_required
def create_challenge():
    form = CreateChallengeForm()
    if form.validate_on_submit():
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
            user_id=current_user.id  # Assuming current_user is from Flask-Login
        )
        db.session.add(challenge)
        db.session.commit()
        flash('Your challenge has been created!', 'success')
        return redirect(url_for('challenge_list'))
    return render_template('create_challenge.html', title='Create Challenge', form=form)

@app.route('/view_challenges')
def challenge_list():
    challenges = Challenge.query.all()
    return render_template('challenge_list.html', challenges=challenges)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(debug=True)
