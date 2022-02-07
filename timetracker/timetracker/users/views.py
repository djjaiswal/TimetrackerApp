from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user,current_user
from timetracker.models import Employee, Project



users = Blueprint('users', __name__)

@users.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        id = request.form.get("empid")
        password = request.form.get("password")
        user = Employee.query.filter_by(emp_id=id).first()
        if user !=None and user.check_password(password):
            login_user(user, remember=True)
            if user.is_admin:
                return redirect(url_for('admin.admin_dashboard'))
            else:
                return redirect(url_for('users.dashboard'))
        else:
            flash('Invalid email or password.')
    return render_template("users/login.html", title='Login')

@users.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('users.login'))

@users.route("/dashboard")
@login_required
def dashboard():
    projects = Project.query.filter_by(project_manager=current_user.emp_id).order_by(Project.date.desc()).all()
    employees = []

    for p in projects:
        tasks = p.tasks
        for t in tasks:
            assignee = t.assignee
            if assignee not in employees:
                employees.append(assignee)
    reporting_employees = [Employee.query.filter_by(emp_id=e).first() for e in employees ]

    return render_template("users/dashboard.html", title="Dashboard", projects = projects)