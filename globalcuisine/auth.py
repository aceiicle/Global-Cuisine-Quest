# globalcuisine/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from .forms import RegistrationForm, LoginForm
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Undesired behavior: Does not redirect to the dashboard page upon successful login
    """
    Handle the login functionality.

    This function is responsible for rendering the login page and processing the login form.
    If the form is submitted and valid, it redirects the user to the dashboard page.
    If the form is not submitted or invalid, it renders the login page with the form.

    Returns:
        If the form is submitted and valid, it redirects to the dashboard page.
        If the form is not submitted or invalid, it renders the login page with the form.
    """
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        return redirect(url_for('main.dashboard'))

    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    return 'Logout'

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register a new user.

    This function handles the registration process for new users. It validates the registration form,
    creates a new user if the form is valid, and redirects the user to the login page after successful registration.

    Returns:
        A rendered template for the registration page if the form is not valid.
        A redirect to the login page if the form is valid and the user is successfully registered.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        form.create_user()

        flash('Account created successfully!', 'success')
        return redirect(url_for('auth.login'))  # Redirect to the login page

    return render_template('register.html', form=form)