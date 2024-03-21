import os

class Config(object):
    # Secret key for signing cookies
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'change-this'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///globalcuisine.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
