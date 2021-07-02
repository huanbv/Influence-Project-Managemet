from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired


class SignUpForm(FlaskForm):
    inputFirstName = StringField('First Name',
                                 [DataRequired(message="please enter your first name!")])
    inputLastName = StringField('Last Name',
                                [DataRequired(message="please enter your last name!")])
    inputEmail = StringField('Email Address',
                             [DataRequired(message="please enter your E-mail Address!")])
    inputPassword = PasswordField('Password',
                                  [InputRequired(message="please enter your password!"),
                                   EqualTo('inputConfirmPassword', message="password does not match!")])
    inputConfirmPassword = PasswordField('Confirm Password')
    submit = SubmitField('Sign Up')


class SignInForm(FlaskForm):
    inputEmail = StringField('Email Address', [DataRequired(message="Please enter your email address")])
    inputPassword = PasswordField('Password',
                                  [EqualTo('inputPassword', message="password does not!")])
    submit = SubmitField('Sign In')


class TaskForm(FlaskForm):
    inputDescription = StringField('Task Description', [DataRequired(message="Please enter your task content!")])
    inputPriority = SelectField('Priority', coerce=int)

    submit = SubmitField('Create Task')
