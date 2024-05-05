from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from .models import User
from wtforms.widgets import html_params
from markupsafe import Markup, escape
from . import db

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already in use. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Please choose a different one.')

    def create_user(self):
        user = User(username=self.username.data, email=self.email.data)
        user.set_password(self.password.data)
        db.session.add(user)
        db.session.commit()

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('That username does not exist. Please register.')
    
    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.check_password(password.data):
            raise ValidationError('Incorrect password.')
        
class StarRatingWidget(object):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.name)
        kwargs.setdefault('class', 'rateyo')
        html = Markup(f'<div {html_params(**kwargs)}></div>')
        html += Markup(f'<input type="hidden" name="{field.name}" value="{field._value()}">')
        return html
    
class StarField(StringField):
    widget = StarRatingWidget()

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = float(valuelist[0])
        else:
            self.data = 0.0

class CreateChallengeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    cuisine_type = SelectField('Cuisine Type', choices=[('option1', 'Option 1'), ('option2', 'Option 2')], validators=[DataRequired()])
    difficulty_level = StarField('Difficulty Level', validators=[DataRequired()])
    submit = SubmitField('Create')