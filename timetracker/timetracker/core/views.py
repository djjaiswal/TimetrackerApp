from flask import Blueprint, redirect,url_for, render_template, flash, abort
from ..models import Task,Employee
from .forms import TaskForm
from timetracker.models import Project
from flask_login import login_required, current_user

core = Blueprint('core', __name__)


def if_manager():
    """
    Prevent non-managers from accessing the page
    """
    if not current_user.is_manager:
        abort(403)

@core.route("/", methods=["GET", "POST"])
@login_required
def homepage():
    return redirect(url_for("users.dashboard"))

@core.route("/projects/<int:project_id>/tasks", methods=["GET", "POST"])
@login_required
def tasklist(project_id):
    if_manager()
    project = Project.query.get(project_id)
    department = project.department_belong_to

    form = TaskForm()
    tasks = project.tasks
    if form.validate_on_submit():
        newtask = Task(name=form.name.data)
        newtask.project_id = project.id
        assignee = Employee.query.filter_by(emp_id = form.assignee.data).first()

        if not assignee or assignee.department_id != department.id:
            flash(f'Employee with ID {form.assignee.data} not found in this Department.')
            return redirect(url_for("core.tasklist", project_id=project_id))

        newtask.assignee = assignee.emp_id

        try:
            newtask.save_to_db()
            flash('You have successfully added a new task.')
        except:
            flash('Oops: Something went wrong, Please try again.')

        return redirect(url_for("core.tasklist",  project_id=project_id))
    return render_template("core/tasklist.html", form= form, tasks = tasks, title=project.name)
