from sqlalchemy.orm import relationship

from main import db
from sqlalchemy import Sequence, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    user_id = db.Column(db.Integer, Sequence('user_id_seg'), primary_key=True)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<User full name is {} {}, email:{}>'.format(self.first_name, self.last_name, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    task_id = db.Column(db.Integer, Sequence('task_id_seq'), primary_key=True)

    description = db.Column(db.String(255), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)

    priority_id = db.Column(db.Integer, ForeignKey('priority.priority_id'))
    priority = relationship('Priority', backref='tasks')

    status_id = db.Column(db.Integer, ForeignKey('status.status_id'))
    status = relationship('Status', backref='tasks')

    project_id = db.Column(db.Integer, ForeignKey('project.project_id'))
    project = relationship('Project', backref='tasks')

    def __repr__(self):
        return '<Task: {} of user {}>'.format(self.description, self.user_id)

    def get_priority_class(self):
        if self.priority_id == 1:
            return "bg-danger"
        elif self.priority_id == 2:
            return "bg-warning"
        elif self.priority_id == 3:
            return "bg-info"
        else:
            return "bg-primary"


class Priority(db.Model):
    priority_id = db.Column(db.Integer, Sequence('priority_id_seq'), primary_key=True)
    text = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Priority: {} with {}>'.format(self.priority_id, self.text)


class Project(db.Model):
    project_id = db.Column(db.Integer, Sequence('project_id_seq'), primary_key=True)

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer, ForeignKey('user.user_id'))
    user = relationship('User', backref='projects')

    status_id = db.Column(db.Integer, ForeignKey('status.status_id'))
    status = relationship('Status', backref='projects')

    def __repr__(self):
        return '<Project: {} of user {}>'.format(self.name, self.description,self.deadline, self.user_id)


class Status(db.Model):
    status_id = db.Column(db.Integer, Sequence('status_id_seq'), primary_key=True)
    description = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Project: {} with {}>'.format(self.status_id, self.description)
