from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError,SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from ..models import Employee, Department


class TaskForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Task Title', validators=[DataRequired()])
    assignee = StringField('Assignee Employee ID', validators=[DataRequired()])
    submit = SubmitField('Submit')