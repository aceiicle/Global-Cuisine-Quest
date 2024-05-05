# globalcuisine/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from .forms import RegistrationForm, LoginForm
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.

    If the request method is POST, it checks the provided credentials against the database.
    If the credentials are valid, it returns a JSON response with a success message.
    If the credentials are invalid, it returns a JSON response with an error message and a 401 status code.

    If the request method is GET, it renders the login form.

    Returns:
        If the request method is POST:
            A JSON response with a success message if the login is successful.
            A JSON response with an error message and a 401 status code if the login fails.
        If the request method is GET:
            The rendered login form.
    """
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            return jsonify({'message': 'Login successful!'})
        else:
            return jsonify({'message': 'Invalid credentials!'}), 401
    else:
        form = LoginForm()
        return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    return 'Logout'

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register a new user.

    This function handles the registration process for new users. It validates the registration form,
    creates a new user account, and redirects the user to the login page upon successful registration.

    Returns:
        A rendered template for the registration page if the request method is 'GET'.
        A redirect to the login page if the registration form is successfully submitted.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username
        email = form.email
        password = form.password

        form.validate_username(username)

        form.validate_email(email)

        form.create_user()

        flash('Account created successfully!', 'success')
        return redirect(url_for('auth.login'))  # Redirect to the login page

    return render_template('register.html', form=form)