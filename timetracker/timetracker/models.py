import enum
from datetime import datetime

from timetracker import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(user_id)



class Employee(db.Model, UserMixin):
    __tablename__ = 'employees'

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True)
    emp_id = db.Column(db.String(64),unique=True,index=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))

    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    projects =db.relationship('Project', backref='pm',
                                lazy='dynamic')
    tasks = db.relationship("Task", backref = "assigned_to",lazy='dynamic')

    is_admin = db.Column(db.Boolean, default=False)
    is_manager = db.Column(db.Boolean, default=False)


    def __init__(self, email, emp_id, first_name,last_name,password):
        self.email = email
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = generate_password_hash(password=password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"Username {self.emp_id}"



class Department(db.Model):
    # Create a Department table
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')
    projects = db.relationship('Project', backref='department_belong_to', lazy=True)

    def __init__(self,name):
        self.name = name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Department: {}>'.format(self.name)


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), )
    project_manager = db.Column(db.String, db.ForeignKey('employees.emp_id'), )
    tasks = db.relationship('Task', backref='project_belong_to', lazy=True)

    def __init__(self,name):
        self.name = name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Project: {}>'.format(self.name)


class TaskStatus(enum.Enum):
    CREATED = 0
    ACKNOWLEDGED = 1
    INPROGRESS = 2
    COMPLETED = 3


class Task(db.Model):

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    date = db.Column(db.DateTime, nullable=False, default=datetime.today())
    status = db.Column(db.Integer(),default=TaskStatus.CREATED.value)

    assignee = db.Column(db.String, db.ForeignKey('employees.emp_id'), )
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), )



    def __init__(self,name):
        self.name = name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Task: {}>'.format(self.name)
