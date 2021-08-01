from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
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


class InfluenceForm(FlaskForm):
    inputStageName = StringField('Stage Name', [DataRequired(message="Please enter your Stage name")])
    inputJoinDate = DateTimeLocalField('Join Date', format='%Y-%m-%dT%H:%M',
                                       validators=[DataRequired(message="Please enter join date!")])
    inputNote = StringField('Influence Note')
    inputGender = StringField('Your Gender', [DataRequired(message="Please enter your gender")])
    inputAge = StringField('Your Age', [DataRequired(message="Please enter your age")])
    inputDateOfBirth = DateTimeLocalField('Date of Birth', format='%Y-%m-%dT%H:%M',
                                          validators=[DataRequired(message="Please enter your data of birth!")])
    inputPhoneNumber = StringField('Your Phone Number', [DataRequired(message="Please enter your phone number")])
    inputEmailAddress = StringField('Email Address', [DataRequired(message="Please enter your email address")])
    inputCountry = StringField('Your Country', [DataRequired(message="Please enter your country")])
    inputCity = StringField('Your City', [DataRequired(message="Please enter your city")])
    inputAddress = StringField('Your Address', [DataRequired(message="Please enter your address")])
    inputCareerName = StringField('Your Career', [DataRequired(message="Please enter your career")])
    inputIncomeRange = StringField('Your Income Range', [DataRequired(message="Please enter your Income Range")])
    inputAvatarUrl = FileField('Avatar Url')
    inputInfluenceStatus = SelectField('Influence Status', coerce=int)


class InfluenceSocialForm(FlaskForm):
    inputSocialName = StringField('Social Name', [DataRequired(message="Please enter your social name!")])
    inputSocialLink = StringField('Social Link', [DataRequired(message="Please enter your social link!")])
    inputSocialFollowers = StringField('Social Followers', [DataRequired(message="Please enter your social followers!")])

    inputInfluence = SelectField('Influence', coerce=int)




