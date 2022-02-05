from flask import render_template, Blueprint, redirect, url_for, abort, flash
from wtforms import SelectField
from wtforms.validators import DataRequired

from timetracker.models import Employee, Department, Project
from .forms import RegistrationForm, DepartmentForm,ProjectForm
from flask_login import login_required, current_user

admin = Blueprint('admin', __name__)

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


@admin.route("/register", methods=["GET", "POST"])
def register():
    check_admin()
    form = RegistrationForm()
    if form.validate_on_submit():
        emp_id = form.emp_id.data
        emp = Employee.query.filter_by(emp_id=emp_id).first()
        if emp:
            flash(f" Employee ID {emp_id} already assigned to Employee {emp.first_name} {emp.last_name}")
            return redirect(url_for('admin.register'))
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = form.password.data
        emp = Employee(email ,emp_id, first_name, last_name, password )
        dep_id = int(form.department.data)
        emp.department =Department.query.get(dep_id)
        emp.save_to_db()
        return redirect(url_for('admin.list_employees'))

    return render_template("admin/register.html", form=form, title='Register')



@admin.route("/adminDashboard", methods=["GET"])
@login_required
def admin_dashboard():
    check_admin()
    return render_template("admin/dasboard.html",title=" Admin Dashborad")


@admin.route("/departments", methods=["GET", "POST"])
@login_required
def list_departments():
    check_admin()
    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data)
        try:
            department.save_to_db()
            flash('You have successfully added a new department.')
        except:
            already_exist = Department.query.filter_by(name= form.name.data )
            if already_exist:
                flash('Error: Department Already exists.')
            else:
                flash('Oops: Something went wrong, Please try again.')
        return redirect(url_for("admin.list_departments"))
    dep = Department.query.all()
    return  render_template("admin/departments.html",departments = dep, form=form , title="Departments")


@admin.route("/departments/<int:id>", methods=["GET", "POST"])
@login_required
def departmentpage(id):
    check_admin()
    department = Department.query.get(id)
    projects = Project.query.filter_by(department_belong_to=department).order_by(Project.date.desc()).all()
    form = ProjectForm()
    if form.validate_on_submit():
        newproject = Project(name=form.name.data)
        newproject.department_id = department.id
        manager = Employee.query.filter_by(emp_id = form.manager.data).first()

        if not manager or manager.department_id != id:
            flash(f'Employee with ID {form.manager.data} not found in this Department.')
            return redirect(url_for("admin.departmentpage", id=id))

        newproject.project_manager = manager.emp_id

        try:
            manager.is_manager = True
            newproject.save_to_db()
            flash('You have successfully added a new department.')
        except:
            flash('Oops: Something went wrong, Please try again.')

        return redirect(url_for("admin.departmentpage", id=id))
    return render_template("admin/departmentpage.html",
                           department = department,
                           projects = projects,
                           form = form,
                           title=department.name)


@admin.route("/employees", methods=["GET", "POST"])
@login_required
def list_employees():
    check_admin()
    employees = Employee.query.all()
    return render_template("admin/list_employees.html",employees=employees, title=" Employees")