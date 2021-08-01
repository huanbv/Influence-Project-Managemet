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
        return '<Project: {} of user {}>'.format(self.name, self.description, self.deadline, self.user_id)


class Status(db.Model):
    status_id = db.Column(db.Integer, Sequence('status_id_seq'), primary_key=True)
    description = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Project: {} with {}>'.format(self.status_id, self.description)


class InfluenceStatus(db.Model):
    kol_status_id = db.Column(db.Integer, Sequence('kol_status_id_seq'), primary_key=True)
    description = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<InfluenceStatus: {} with {}>'.format(self.kol_status_id, self.description)


class InfluenceSocial(db.Model):
    kol_social_id = db.Column(db.Integer, Sequence('kol_social_id_seq'), primary_key=True)

    social_name = db.Column(db.String(50), nullable=False)
    social_link = db.Column(db.String(255), nullable=False)
    social_followers = db.Column(db.String(50), nullable=False)

    kol_id = db.Column(db.Integer, ForeignKey('influence.kol_id'))
    influence = relationship('Influence', backref='influenceSocials')

    def __repr__(self):
        return '<InfluenceSocial: {} of user {}>'.format(self.social_name, self.social_link, self.social_followers, self.user_id)


class Influence(db.Model):
    __searchable__ = ['stage_name', 'note']
    kol_id = db.Column(db.Integer, Sequence('kol_id_seq'), primary_key=True)

    avatar_url = db.Column(db.String(255))
    stage_name = db.Column(db.String(50), nullable=False)
    join_date = db.Column(db.DateTime, nullable=False)
    note = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    age = db.Column(db.String(50), nullable=False)
    data_of_birth = db.Column(db.DateTime, nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    email_address = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    career_name = db.Column(db.String(50), nullable=False)
    income_range = db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, ForeignKey('user.user_id'))
    user = relationship('User', backref='influences')

    kol_status_id = db.Column(db.Integer, ForeignKey('influence_status.kol_status_id'))
    influence_status = relationship('InfluenceStatus', backref='influences')

    def __repr__(self):
        return '<Influences: {} of user {}>'.format(self.avatar_url, self.stage_name, self.join_date, self.note, self.gender, self.age,
                                                    self.data_of_birth, self.phone_number, self.email_address,
                                                    self.country, self.city, self.city, self.address, self.career_name,
                                                    self.income_range, self.user_id)

    def get_influence_status_class(self):
        if self.kol_status_id == 1:
            return "bg-info"
        elif self.kol_status_id == 2:
            return "bg-warning"
        elif self.kol_status_id == 3:
            return "bg-danger"
        else:
            return "bg-primary"


