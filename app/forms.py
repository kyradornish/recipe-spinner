from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField, SelectField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
import os
import requests

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def vaildate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class RecipeSearch(FlaskForm):
    ingredient = StringField('Ingredient: ', validators=[DataRequired()])
    submit = SubmitField('Submit')

def getRecipeByIngredients(ingredients):
    payload = {
        'fillIngredients': False,
        'ingredients': ingredients,
        'limitLicense': False,
        'number': 6,
        'ranking': 1
    }

    endpoint = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients"

    headers = {
        "X-Mashape-Key": "OcWXtWKiwJmsh9je6Ev8yYDRO2Bpp1bHFrqjsnMcAjT0dmqtZg",
        "X-Mashape-Host": "spoonacular-recipe-food-nutrition-v1.p.mashape.com"
    }

    r = requests.get(endpoint, params=payload, headers=headers)
    results = r.json()

    return results

def getRecipeURL(id):
    payload = {
        'id': id
    }

    endpoint = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{}/information".format(id)

    headers = {
        "X-Mashape-Key": "OcWXtWKiwJmsh9je6Ev8yYDRO2Bpp1bHFrqjsnMcAjT0dmqtZg",
        "X-Mashape-Host": "spoonacular-recipe-food-nutrition-v1.p.mashape.com"
    }

    r = requests.get(endpoint, params=payload, headers=headers)
    results = r.json()

    return results
