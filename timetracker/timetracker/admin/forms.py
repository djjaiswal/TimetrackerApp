from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError,SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from ..models import Employee, Department


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    deps = Department.query.all()
    dnames = [(d.id, d.name) for d in deps]

    email = StringField('Email', validators=[DataRequired(), Email()])
    emp_id = StringField('employee ID', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    department = SelectField('Department', validators=[DataRequired()], choices=dnames, validate_choice=False)

    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')



class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ProjectForm(FlaskForm):

    name = StringField('Project Title', validators=[DataRequired()])
    manager = StringField('Manager Employee ID', validators=[DataRequired()])
    submit = SubmitField('Submit')