from flask import render_template, Blueprint, redirect, url_for, abort, flash, request
from timetracker import db
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

    if request.method == "POST":
        empid = request.form.get("empid")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        department = request.form.get("departments")
        password = request.form.get("password")
        email = request.form.get("email")
        emp = Employee.query.filter_by(emp_id=empid).first()
        if emp:
            flash(f" Employee ID {empid} already assigned to Employee {emp.first_name} {emp.last_name}")
            return redirect(url_for('admin.register'))


        emp = Employee(email ,empid, fname, lname, password)
        dep_id = int(department)
        emp.department =Department.query.get(dep_id)
        emp.save_to_db()
        flash(f"Employee {empid} added succesfully ")
        return redirect(url_for('admin.list_employees'))
    deps = Department.query.all()
    return render_template("admin/register.html", departments=deps, title='Register')



@admin.route("/adminDashboard", methods=["GET"])
@login_required
def admin_dashboard():
    check_admin()
    deps = Department.query.all()
    emps = Employee.query.all()
    projs= Project.query.all()
    return render_template("admin/dasboard.html", dep=len(deps),emp=len(emps),proj=len(projs),title=" Admin Dashborad")


@admin.route("/departments", methods=["GET", "POST"])
@login_required
def list_departments():
    check_admin()
    if request.method == "POST":
        name = request.form.get("department-name")
        existing = Department.query.filter_by(name = name).first()
        if not existing:
            newdep = Department(name=name)
            newdep.save_to_db()
        else:
            flash(" Department already exist", "error")
        return redirect(url_for("admin.list_departments"))
    dep = Department.query.all()
    return  render_template("admin/departments.html",departments = dep, title="Departments")

@admin.route("/departments/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_departemnt(id):
    if request.method == "POST":
        department = Department.query.get(id)
        for proj in department.projects:
            project = Project.query.get(proj.id)
            db.session.delete(project)
            db.session.commit()
        db.session.delete(department)
        db.session.commit()
    return redirect (url_for("admin.list_departments"))

@admin.route("/departments/<int:id>", methods=["GET", "POST"])
@login_required
def departmentpage(id):
    check_admin()
    department = Department.query.get(id)
    projects = Project.query.filter_by(department_belong_to=department).order_by(Project.date.desc()).all()

    if request.method == "POST":
        newproject = Project(name=request.form.get("name"))
        newproject.department_id = department.id
        manager = Employee.query.filter_by(emp_id = request.form.get("manager-id")).first()

        if not manager or manager.department_id != id:
            flash(f'Employee with ID {request.form.get("manager-id")} not found in this Department.')
            return redirect(url_for("admin.departmentpage", id=id))

        newproject.project_manager = manager.emp_id

        try:
            manager.is_manager = True
            newproject.save_to_db()
            flash('You have successfully added a new department.' , "success")
        except:
            flash('Oops: Something went wrong, Please try again.')

        return redirect(url_for("admin.departmentpage", id=id))
    return render_template("admin/departmentpage.html",
                           department = department,
                           projects = projects,
                           title=department.name)



@admin.route("/employees", methods=["GET", "POST"])
@login_required
def list_employees():
    check_admin()
    employees = Employee.query.all()
    return render_template("admin/list_employees.html",employees=employees, title=" Employees")