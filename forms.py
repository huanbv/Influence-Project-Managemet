from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.fields.html5 import DateTimeLocalField
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
    inputPassword = PasswordField('Password', [EqualTo('inputPassword', message="password does not!")])
    submit = SubmitField('Sign In')


class TaskForm(FlaskForm):
    inputDescription = StringField('Task Description', [DataRequired(message="Please enter your task content!")])
    inputDeadline = DateTimeLocalField('Project Deadline', format='%Y-%m-%dT%H:%M', validators=[DataRequired(message="Please enter your task dateline!")])

    inputPriority = SelectField('Priority', coerce=int)
    inputStatus = SelectField('Status', coerce=int)
    inputProject = SelectField('Project', coerce=int)

    # custom validation
    def validate(self):
        if not FlaskForm.validate(self):
            return False

        import models
        the_project = models.Project.query.get(self.inputProject.data)

        if self.inputDeadline.data > the_project.deadline:
            self.inputDeadline.errors.append(f'Deadline cannot longer than its parent project ({the_project.deadline})')
            return False

        return True


class ProjectForm(FlaskForm):
    inputName = StringField('Project Name', [DataRequired(message="Please enter your project name!")])
    inputDescription = StringField('Project Description', [DataRequired(message="Please enter your project content!")])
    inputDeadline = DateTimeLocalField('Project Deadline', format='%Y-%m-%dT%H:%M', validators=[DataRequired(message="Please enter your project dateline!")])

