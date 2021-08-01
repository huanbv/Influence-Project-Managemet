from flask import Flask, render_template, request, flash, session
from werkzeug.utils import redirect

from forms import SignUpForm, SignInForm, TaskForm, ProjectForm, InfluenceForm, InfluenceSocialForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PN Python-Flask Web App'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
search = Search()
search.init_app(app)
migrate = Migrate()
with app.app_context():
    # allow dropping column for sqlite
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

import models


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/')
# def main():
#     _user_id = session.get('user')
#     if _user_id:
#         return redirect('/userInfluence')
#
#     return render_template('index.html')


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/myAccount', methods=['GET', 'POST'])
def myAccount():
        _user_id = session.get('user')
        if _user_id:
            user = db.session.query(models.User).filter_by(user_id=_user_id).first()
            return render_template('profile.html', user=user)
        else:
            return redirect('/')


@app.route('/signUp', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        print("validate on submit")
        _firstName = form.inputFirstName.data
        _lastName = form.inputLastName.data
        _email = form.inputEmail.data
        _password = form.inputPassword.data

        if(db.session.query(models.User).filter_by(email=_email).count() == 0):
            user = models.User(first_name=_firstName, last_name=_lastName, email=_email)
            user.set_password(_password)

            # backref
            # user.tasks

            db.session.add(user)
            db.session.commit()
            return render_template('signUpSuccess.html', user=user)
        else:
            flash('Email {} is already exit!'.format(_email))
            return render_template('signup.html', form=form)

    print("Not validate on submit")
    return render_template('signup.html', form=form)


@app.route('/signIn', methods=['GET', 'POST'])
def signin():
    _user_id = session.get('user')
    if _user_id:
        return redirect('/userInfluence')

    else:
        form = SignInForm()

        if form.validate_on_submit():
            _email = form.inputEmail.data
            _password = form.inputPassword.data

            user = db.session.query(models.User).filter_by(email=_email).first()
            if (user is None):
               flash('Wrong email address or password')
            else:
                if (user.check_password(_password)):
                    session['user'] = user.user_id
                    return redirect('userHome')
                else:
                    flash('Wrong email address or password')

        return render_template('signin.html', form=form)


@app.route('/userHome', methods=['GET', 'POST'])
def userHome():
        _user_id = session.get('user')
        if _user_id:
            user = db.session.query(models.User).filter_by(user_id=_user_id).first()
            return render_template('projects/userhome.html', user=user)
        else:
            return redirect('/')


@app.route('/userInfluence', methods=['GET', 'POST'])
def userInfluence():
        _user_id = session.get('user')
        if _user_id:
            user = db.session.query(models.User).filter_by(user_id=_user_id).first()
            return render_template('influences/influence.html', user=user)
        else:
            return redirect('/')


@app.route('/influence/results', methods=['GET', 'POST'])
def results():
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        search_word = request.args.get('search')
        the_influence = influence.query.msearch(search_word, fields=['stage_name', 'note'], limit=5)
        return render_template('influences/result.html', Influence=the_influence, user=user)
    else:
        return redirect('/')


@app.route('/logOut')
def logOut():
    session.clear();
    return redirect('/')


@app.route('/newTask', methods=['GET', 'POST'])
def newTask():
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()

        form = TaskForm()
        form.inputPriority.choices = [(p.priority_id, p.text) for p in db.session.query(models.Priority).all()]
        form.inputStatus.choices = [(p.status_id, p.description) for p in db.session.query(models.Status).all()]
        form.inputProject.choices = [(p.project_id, p.name) for p in db.session.query(models.Project).filter_by(user_id=_user_id).all()]

        if form.validate_on_submit():
            task = models.Task(
                description=form.inputDescription.data,
                deadline=form.inputDeadline.data,
                priority_id=form.inputPriority.data,
                project_id=form.inputProject.data,
                status_id=1
            )

            db.session.add(task)
            db.session.commit()
            return redirect('/userHome')

        form.inputStatus.render_kw = {'readonly': 'true', 'style': 'pointer-events: none'}
        return render_template('projects/newtask.html', form=form, user=user)

    return redirect('/')


@app.route('/task/edit/<int:task_id>', methods=['GET', 'POST'])
def editTask(task_id):
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()

        form = TaskForm()
        form.inputPriority.choices = [(p.priority_id, p.text) for p in db.session.query(models.Priority).all()]
        form.inputStatus.choices = [(p.status_id, p.description) for p in db.session.query(models.Status).all()]
        form.inputProject.choices = [(p.project_id, p.name) for p in db.session.query(models.Project).filter_by(user_id=_user_id).all()]

        the_task = db.session.query(models.Task).filter_by(task_id=task_id).first()

        if form.validate_on_submit():
            the_task.description = form.inputDescription.data
            the_task.deadline = form.inputDeadline.data
            the_task.priority_id = form.inputPriority.data
            the_task.project_id = form.inputProject.data
            the_task.status_id = form.inputStatus.data
            db.session.commit()

            # invoking this to update the associated project status
            update_project_status(the_task.project)
            return redirect(f"/project/{request.args.get('project_id')}")

        form.inputDescription.default = the_task.description
        form.inputDeadline.default = the_task.deadline
        form.inputPriority.default = the_task.priority_id
        form.inputStatus.default = the_task.status_id
        form.inputProject.default = the_task.project_id
        form.process()
        return render_template('projects/newtask.html', form=form, user=user)

    return redirect('/')


def update_project_status(the_project):
    in_progress_tasks = list(filter(lambda task: task.status_id == 2, the_project.tasks))
    # at least 1 in progress task is exists
    if len(in_progress_tasks) >= 1:
        the_project.status_id = 2
        db.session.commit()
        return

    finished_tasks = list(filter(lambda task: task.status_id == 4, the_project.tasks))
    # all the tasks in the_project have completed
    if len(finished_tasks) == len(the_project.tasks):
        the_project.status_id = 4
        db.session.commit()
        return

    # otherwise, it's not started
    the_project.status_id = 1
    db.session.commit()


@app.route('/task/delete/<int:task_id>', methods=['GET', 'POST'])
def deleteTask(task_id):
    _user_id = session.get('user')
    if _user_id:

        task = db.session.query(models.Task).filter_by(task_id=task_id).first()
        db.session.delete(task)
        db.session.commit()
        return redirect(f"/project/{request.args.get('project_id')}")

    return redirect('/')


@app.route('/newProject', methods=['GET', 'POST'])
def newProject():
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()

        form = ProjectForm()
        if form.validate_on_submit():
            _name = form.inputName.data
            _description = form.inputDescription.data
            _deadline = form.inputDeadline.data

            project = models.Project(name=_name, description=_description, deadline=_deadline, user=user, status_id=1)
            db.session.add(project)
            db.session.commit()
            return redirect('/')

        return render_template('projects/newproject.html', form=form, user=user)

    return redirect('/')


@app.route('/project/edit/<int:project_id>', methods=['GET', 'POST'])
def editProject(project_id):
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()

        the_project = db.session.query(models.Project).get(project_id)
        form = ProjectForm()

        if form.validate_on_submit():
            the_project.name = form.inputName.data
            the_project.description = form.inputDescription.data
            the_project.deadline = form.inputDeadline.data
            the_project.user_id = _user_id
            db.session.commit()
            return redirect('/')

        # gan du lieu cu ra form de chinh sua
        form.inputName.data = the_project.name
        form.inputDescription.data = the_project.description
        form.inputDeadline.data = the_project.deadline
        return render_template('projects/newproject.html', form=form, user=user)

    return redirect('/')


@app.route('/project/delete/<int:project_id>', methods=['GET', 'POST'])
def deleteProject(project_id):
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()

        the_project = db.session.query(models.Project).get(project_id)
        db.session.delete(the_project)
        db.session.commit()
        return redirect('/', user=user)

    return redirect('/')


@app.route('/project/<int:project_id>', methods=['GET'])
def project(project_id):

    _user_id = session.get('user')
    if _user_id:

        user = db.session.query(models.User).filter_by(user_id=_user_id).first()

        the_project = db.session.query(models.Project).get(project_id)
        if not the_project.user_id == user.user_id:
            flash('You don\'t own this Project')
            return redirect('/')

        return render_template('projects/project.html', project=the_project,  user=user)

    return redirect('/')


@app.route('/newInfluence', methods=['GET', 'POST'])
def newInfluence():
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()

        form = InfluenceForm()
        form.inputInfluenceStatus.choices = [(p.kol_status_id, p.description) for p in
                                             db.session.query(models.InfluenceStatus).all()]

        if form.validate_on_submit():
            _avatar_url = form.inputAvatarUrl.data
            _stage_name = form.inputStageName.data
            _join_date = form.inputJoinDate.data
            _note = form.inputNote.data
            _gender = form.inputGender.data
            _age = form.inputAge.data
            _data_of_birth = form.inputDateOfBirth.data
            _phone_number = form.inputPhoneNumber.data
            _email_address = form.inputEmailAddress.data
            _country = form.inputCountry.data
            _city = form.inputCity.data
            _address = form.inputAddress.data
            _career_name = form.inputCareerName.data
            _income_range = form.inputIncomeRange.data
            _kol_status_description = form.inputInfluenceStatus.data

            influence = models.Influence(avatar_url=_avatar_url, stage_name=_stage_name, join_date=_join_date, note=_note, gender=_gender,
                                         age=_age, data_of_birth=_data_of_birth, phone_number=_phone_number,
                                         email_address=_email_address, country=_country, city=_city, address=_address,
                                         career_name=_career_name, income_range=_income_range, user=user,
                                         kol_status_id=_kol_status_description)
            db.session.add(influence)
            db.session.commit()
            return redirect('/userInfluence')

        return render_template('influences/newInfluencer.html', form=form, user=user)

    return redirect('/userInfluence')


@app.route('/influence/edit/<int:kol_id>', methods=['GET', 'POST'])
def editInfluence(kol_id):
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()

        # the_influence = db.session.query(models.Influence).get(kol_id)
        form = InfluenceForm()
        form.inputInfluenceStatus.choices = [(p.kol_status_id, p.description) for p in
                                             db.session.query(models.InfluenceStatus).all()]

        the_influence = db.session.query(models.Influence).filter_by(kol_id=kol_id).first()

        if form.validate_on_submit():
            the_influence.stage_name = form.inputStageName.data
            the_influence.join_date = form.inputJoinDate.data
            the_influence.note = form.inputNote.data
            the_influence.gender = form.inputGender.data
            the_influence.age = form.inputAge.data
            the_influence.data_of_birth = form.inputDateOfBirth.data
            the_influence.phone_number = form.inputPhoneNumber.data
            the_influence.email_address = form.inputEmailAddress.data
            the_influence.country = form.inputCountry.data
            the_influence.city = form.inputCity.data
            the_influence.address = form.inputAddress.data
            the_influence.career_name = form.inputCareerName.data
            the_influence.income_range = form.inputIncomeRange.data
            the_influence.kol_status_id = form.inputInfluenceStatus.data
            the_influence.user_id = _user_id
            db.session.commit()
            return redirect('/userInfluence')

        # gan du lieu cu ra form de chinh sua
        form.inputStageName.default = the_influence.stage_name
        form.inputJoinDate.default = the_influence.join_date
        form.inputNote.default = the_influence.note
        form.inputGender.default = the_influence.gender
        form.inputAge.default = the_influence.age
        form.inputDateOfBirth.default = the_influence.data_of_birth
        form.inputPhoneNumber.default = the_influence.phone_number
        form.inputEmailAddress.default = the_influence.email_address
        form.inputCountry.default = the_influence.country
        form.inputCity.default = the_influence.city
        form.inputAddress.default = the_influence.address
        form.inputCareerName.default = the_influence.career_name
        form.inputIncomeRange.default = the_influence.income_range
        form.inputInfluenceStatus.default = the_influence.kol_status_id
        form.process()
        return render_template('influences/newInfluencer.html', form=form, user=user)

    return redirect('/userInfluence')


@app.route('/influence/delete/<int:kol_id>', methods=['GET', 'POST'])
def deleteInfluence(kol_id):
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()

        the_influence = db.session.query(models.Influence).get(kol_id)
        db.session.delete(the_influence)
        db.session.commit()
        return redirect('/userInfluence')

    return redirect('/userInfluence')


@app.route('/influence/<int:kol_id>', methods=['GET'])
def influence(kol_id):

    _user_id = session.get('user')
    if _user_id:

        user = db.session.query(models.User).filter_by(user_id=_user_id).first()

        the_influence = db.session.query(models.Influence).get(kol_id)
        if not the_influence.user_id == user.user_id:
            flash('You do not own this influence')
            return redirect('/userInfluence')

        return render_template('influences/influenceSocialList.html', influence=the_influence,  user=user)

    return redirect('/userInfluence')


@app.route('/newInfluenceSocialList', methods=['GET', 'POST'])
def newInfluenceSocialList():
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()

        form = InfluenceSocialForm()
        form.inputInfluence.choices = [(p.kol_id, p.stage_name) for p in
                                       db.session.query(models.Influence).filter_by(user_id=_user_id).all()]

        if form.validate_on_submit():
            influence_social = models.InfluenceSocial(
                social_name=form.inputSocialName.data,
                social_link=form.inputSocialLink.data,
                social_followers=form.inputSocialFollowers.data,
                kol_id=form.inputInfluence.data
            )

            db.session.add(influence_social)
            db.session.commit()
            return redirect('/userInfluence')

        return render_template('influences/newInfluenceSocialLink.html', form=form, user=user)

    return redirect('/userInfluence')


@app.route('/influenceSocial/edit/<int:kol_social_id>', methods=['GET', 'POST'])
def editInfluenceSocial(kol_social_id):
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()

        form = InfluenceSocialForm()
        form.inputInfluence.choices = [(p.kol_id, p.stage_name) for p
                                       in db.session.query(models.Influence).filter_by(user_id=_user_id).all()]

        the_influence_social = db.session.query(models.InfluenceSocial).filter_by(kol_social_id=kol_social_id).first()

        if form.validate_on_submit():
            the_influence_social.social_name = form.inputSocialName.data
            the_influence_social.social_link = form.inputSocialLink.data
            the_influence_social.social_followers = form.inputSocialFollowers.data
            the_influence_social.kol_id = form.inputInfluence.data
            db.session.commit()

            return redirect(f"/influence/{request.args.get('kol_id')}")

        form.inputSocialName.default = the_influence_social.social_name
        form.inputSocialLink.default = the_influence_social.social_link
        form.inputSocialFollowers.default = the_influence_social.social_followers
        form.inputInfluence.default = the_influence_social.kol_id
        form.process()
        return render_template('influences/newInfluenceSocialLink.html', form=form, user=user)

    return redirect('/userInfluence')


@app.route('/influenceSocial/delete/<int:kol_social_id>', methods=['GET', 'POST'])
def deleteInfluenceSocial(kol_social_id):
    _user_id = session.get('user')
    if _user_id:

        influence_social = db.session.query(models.InfluenceSocial).filter_by(kol_social_id=kol_social_id).first()
        db.session.delete(influence_social)
        db.session.commit()
        return redirect(f"/influence/{request.args.get('kol_id')}")

    return redirect('/userInfluence')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)
