from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from .models import User
from wtforms.widgets import html_params
from markupsafe import Markup, escape
from flask_wtf.file import FileField, FileAllowed
from . import db

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        self.user = User.query.filter_by(username=username.data).first()
        if self.user:
            raise ValidationError('That username is already in use. Please choose a different one.')

    def validate_email(self, email):
        self.user = User.query.filter_by(email=email.data).first()
        if self.user:
            raise ValidationError('That email is already in use. Please choose a different one.')

    def create_user(self):
        user = User(username=self.username.data, email=self.email.data)
        user.set_password(self.password.data)
        db.session.add(user)
        db.session.commit()

class LoginForm(FlaskForm):
    username_or_email = StringField('Email or Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_username(self, username_or_email):
        self.user = User.query.filter((User.username==username_or_email.data) | (User.email==username_or_email.data)).first()
        if not self.user:
            raise ValidationError('That username or email does not exist. Please register.')
    
    def validate_password(self, password):
        self.user = User.query.filter((User.username==self.username_or_email.data) | (User.email==self.username_or_email.data)).first()
        if self.user and not self.user.check_password(password.data):
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
    recipe_type = SelectField('Recipe Type', choices=[('Challenge', 'Challenge'),('Family Recipe', 'Family Recipe'), ('Quick and Easy', 'Quick and Easy'), ('One-Pot', 'One-Pot'), ('Budget-Friendly', 'Budget-Friendly')], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    is_recipe = BooleanField('Is Your Post a Recipe?')
    ingredients = TextAreaField('Ingredients')
    recipe_instructions = TextAreaField('Recipe Instructions')
    cuisine_type = SelectField('Cuisine Region', choices=[('North American', 'North American'), ('South American', 'South American'), ('African', 'African'), ('Middle Eastern', 'Middle Eastern'), ('Northern European', 'Northern European'), ('Central European', 'Central European'), ('Eastern European', 'Eastern European'), ('West Asian', 'West Asian'), ('North Asian', 'North Asian'), ('Japanese', 'Japanese'), ('South Asian', 'South Asian'), ('Oceania', 'Oceania')], validators=[DataRequired()])
    cuisine_style = SelectField('Cuisine Style', choices=[('Home Cook', 'Home Cook'),('Fast Food', 'Fast Food'), ('Fusion Cuisine', 'Fusion Cuisine'), ('Grande Cuisine', 'Grande Cuisine'), ('Molecular Gastronomy', 'Molecular Gastronomy'), ('Vegetarian Cuisine', 'Vegetarian Cuisine'), ('Vegan Cuisine', 'Vegan Cuisine'), ('Street Food', 'Street Food'), ('Soul Food', 'Soul Food')], validators=[DataRequired()])
    difficulty_level = StarField('Difficulty Level', validators=[DataRequired()])
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    submit = SubmitField('Create')

class SubmissionForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Submit')

# Add JavaScript to toggle the visibility of the textarea based on the boolean field's value
toggle_script = """
<script>
    function toggleTextArea() {
        var checkbox = document.getElementById('is_recipe');
        var textarea = document.getElementById('recipe_instructions');
        if (checkbox.checked) {
            textarea.style.display = 'block';
        } else {
            textarea.style.display = 'none';
        }
    }
</script>
"""