# globalcuisine/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import RegistrationForm

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/logout')
def logout():
    return 'Logout'

@auth.route('/register')
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Logic to handle form submission
        flash('Account created successfully!', 'success')
        return redirect(url_for('auth.login'))  # Redirect to the login page
    return render_template('register.html', form=form)
