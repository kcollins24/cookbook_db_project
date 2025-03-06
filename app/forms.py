from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField, SubmitField, FieldList, SelectField, TextAreaField
from wtforms.widgets import TextArea
from wtforms.validators import (
        DataRequired, 
        Length,
        EqualTo,
        Optional
)

class SignupForm(FlaskForm):
    name = StringField(
            'Name',
            validators=[DataRequired()]
    )

    password = PasswordField(
            'Password',
            validators=[
                DataRequired(),
                Length(min=6, message='Select a stronger password.')
            ]
    )

    confirm = PasswordField(
            'Confirm Your Password',
            validators=[
                DataRequired(),
                EqualTo('password',message='Passwords must match.')
            ]
    )
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    name = StringField(
            'Name',
            validators=[
                DataRequired()
            ]
    )

    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class CookbookForm(FlaskForm):
    title= StringField(
            'Title',
            validators=[DataRequired()]
    )

    category = StringField(
        'Category',
        validators=[Optional()]
        )
    submit= SubmitField('Create')

class RecipeFromURLForm(FlaskForm):
    url=StringField(
            'url',
            validators=[DataRequired(message='Invalid')]
    )
    submit=SubmitField('Create')

class RecipeForm(FlaskForm):
    title= StringField(
            'Title',
            validators=[DataRequired(message="Invalid")]
    )

    authors= StringField(
            'Author(s)',
            validators=[DataRequired(message="Invalid")]
    )

    url= StringField(
            'url',
            validators=[Optional()]
    )

    cooking_time = StringField(
            'Cooking Time',
            validators=[DataRequired(message="Invalid")]
    )

    amount = StringField(
            'Yield',
            validators=[DataRequired(message="Invalid")]
    )

    ingredients = TextAreaField(
            'Ingredients',
            widget=TextArea(),
            validators=[DataRequired(message="Invalid")]
    )

    instructions = TextAreaField(
            'Instructions',
            widget=TextArea(),
            validators=[DataRequired(message="Invalid")]
    )

    description = StringField(
            'Description',
            validators=[DataRequired(message="Invalid")]
    )

    category = StringField(
            'Category',
            validators=[DataRequired(message="Invalid")]
    )

    main_ingredient = StringField(
            'Main Ingredient',
            validators=[DataRequired(message="Invalid")]
    )
    submit= SubmitField('Submit')

class ReviewForm(FlaskForm):
    comment = StringField(
            'Comment',
            validators=[DataRequired(message="Invalid")]
    )

    stars = SelectField(
            'Number of Stars',
            choices= ['1','2','3','4','5']
    )

    submit= SubmitField('Leave Review')

class SearchForm(FlaskForm):
    search_choice = SelectField(
            'Select Search',
            choices= ['Cookbooks', 'Recipes']
    )
    title = StringField(
            'Title',
            validators=[Optional()]
    )
    category = StringField(
            'Category',
            validators=[Optional()]
    )
    main_ingredient = StringField(
            'Main Ingredient',
            validators=[Optional()]
    )
    min_rating = SelectField(
            'Minimum Rating',
            choices=['0','1','2','3','4'],
            validators=[Optional()]
    )
    submit= SubmitField('Search')
