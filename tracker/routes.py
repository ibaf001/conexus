from flask import render_template, url_for, flash, redirect, request, abort

from tracker import app, db, bcrypt
from tracker import mysql
from tracker.forms import *
from tracker.utils import *
from tracker.models import Employee, User, Project
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route('/projects')
@login_required
def projects():
    all_projects = retrieve_project_by_id(current_user.id)
    return render_template('projects.html', title='All Projects', all_projects=all_projects)


@app.route('/del_project/<case>')
def del_project(case):
    # db.session.query(Project).filter(Project.id == index).delete()
    # db.session.commit()
    remove_project(case)
    return redirect(url_for('projects'))


@app.route('/project/<int:index>')
@login_required
def project(index):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM Project where id = {}'''.format(index))
    row = cur.fetchone()
    emp = Employee(index, row['Jur'], row['Assignee'])
    return render_template('project.html', title='Project', emp=emp)


@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        files = request.files.getlist('file')
        for x in files:
            print(x)
        return 'success'
    else:
        return 'landing to upload page'


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created you are now able to login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


def get_form(name):
    name = name.lower()
    if name == '' or name == 'duke':
        return DukeForm()
    elif name == 'ipl':
        return IPLForm()
    elif name == 'comcast':
        return ComcastForm()
    elif name == 'citizen':
        return CitizenForm()
    else:
        return DukeForm()


@app.route("/add_project/", defaults={'name': 'Duke'}, methods=["GET", "POST"])
@app.route("/add_project/<name>", methods=["GET", "POST"])
@login_required
def add_project(name):
    form = get_form(name)
    clients = ['Duke', 'IPL', 'Comcast', 'Citizen']
    if form.validate_on_submit():
        obj = {}
        for field in form:
            if field.name not in ('csrf_token', 'submit'):
                obj[field.label.text] = field.data
        obj['user_id'] = current_user.id
        obj['client'] = name
        save_project(obj)
        flash('project created successfully', 'success')
        return render_template("add_project.html", form=form, clients=clients, selected=name)
    return render_template("add_project.html", form=form, clients=clients, selected=name)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
def account():
    return render_template('account.html', title='Account')
