from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from random import sample
from . import db
import logging
logging.basicConfig(level=logging.INFO)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    challenges = db.relationship('Challenge', backref='author', lazy=True)
    submissions = db.relationship('Submission', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    submissions = db.relationship('Submission', backref='challenge', lazy=True)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    region = db.Column(db.String(100), nullable=False) # e.g. Asian, European, Australian, South American, North American, African
    cuisine = db.Column(db.String(100), nullable=False) # e.g. Japanese, Italian
    ingredients = db.Column(db.Text, nullable=False) # comma-separated ingredients
    preparation_time = db.Column(db.Integer, nullable=False) # in minutes
    cooking_time = db.Column(db.Integer, nullable=False) # in minutes
    steps = db.Column(db.Text, nullable=False) # comma-separated steps

    def get_random_recipes(target_region, count=3):
        # Get a list of random recipes from the database based on the cuisine
        all_recipes = Recipe.query.filter_by(region=target_region).all()
        logging.info(f"all_recipes for {target_region}: {all_recipes}")
        if len(all_recipes) <= count:
            random_recipes = all_recipes
        else:
            random_recipes = sample(all_recipes, count)

        logging.info(f"random_recipes for {target_region}: {random_recipes}")

        return random_recipes