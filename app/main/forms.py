from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, ValidationError, StringField
from wtforms.validators import Required, Email, DataRequired
from ..models import User


class GoalForm(FlaskForm):
    title = StringField('Pitch Category Title', validators=[DataRequired()])
    body = TextAreaField('Enter your Pitch here', validators=[DataRequired()])
    submit = SubmitField('Submit')

    '''
    crate the inputs for comments form with vite options
    '''


class CommentForm(FlaskForm):
    comment = TextAreaField('Write a comment here',
                            validators=[DataRequired()])

    submit = SubmitField('Submit')

    '''
    crate the inputs for comments form with vote option
    '''


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.', validators=[Required()])
    submit = SubmitField('Submit')
