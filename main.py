from flask import Flask, render_template, request, flash, session
from werkzeug.utils import redirect

from forms import SignUpForm, SignInForm, TaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PN Python-Flask Web App'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models


@app.route('/')
def main():

    todolist = [
        {
            'name': 'Buy milk',
            'description': 'buy 2'
        },
        {
            'name': 'Buy milk 2',
            'description': 'buy 22'
        }
    ]
    return render_template('index.html', todolist=todolist)


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
            return render_template('userhome.html', user=user)
        else:
            return redirect('/')


@app.route('/logOut')
def logOut():
    session.clear();
    return redirect('/')


@app.route('/newTask', methods=['GET', 'POST'])
def newTask():
    _user_id = session.get('user')
    form = TaskForm()
    form.inputPriority.choices = [(p.priority_id, p.text) for p in db.session.query(models.Priority).all()]
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()

        if form.validate_on_submit():
            _description = form.inputDescription.data
            _priority_id = form.inputPriority.data
            priority = db.session.query(models.Priority).filter_by(priority_id=_priority_id).first()

            _task_id = request.form['hiddenTaskId']
            if _task_id == "0":
                task = models.Task(description=_description, user=user, priority=priority)
                db.session.add(task)
            else:
                task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
                task.description = _description
                task.priority = priority

            db.session.commit()
            return redirect('/userHome')

        return render_template('/newtask.html', form=form, user=user)

    return redirect('/')


@app.route('/updateTask', methods=['GET', 'POST'])
def updateTask():
    _user_id = session.get('user')
    form = TaskForm()
    form.inputPriority.choices = [(p.priority_id, p.text) for p in db.session.query(models.Priority).all()]
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        _task_id = request.form['hiddenTaskId']
        if _task_id:
            task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
            form.inputDescription.default = task.description
            form.inputPriority.default = task.priority_id
            form.process()
            return render_template('/newtask.html', form=form, user=user, task=task)

    return redirect('/')


@app.route('/doneTask', methods=['GET', 'POST'])
def doneTask():
    _user_id = session.get('user')
    if _user_id:
        _task_id = request.form['hiddenTaskId']
        if _task_id:
            task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
            task.isCompleted = True
            db.session.commit()

            return redirect('/userHome')

    return redirect('/')


@app.route('/deleteTask', methods=['GET', 'POST'])
def deleteTask():
    _user_id = session.get('user')
    if _user_id:
        _task_id = request.form['hiddenTaskId']
        if _task_id:
            task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
            db.session.delete(task)
            db.session.commit()

            return redirect('/userHome')

        return redirect('/')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)