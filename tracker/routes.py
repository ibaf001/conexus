import os

from flask import render_template, url_for, flash, redirect, request, Markup
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from datetime import datetime
from tracker import app, db, bcrypt
from tracker.forms import *
from tracker.models import User
from tracker.utils import *


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route('/projects', defaults={'page': 1})
@app.route('/projects/<int:page>')
@login_required
def projects(page):
    all_projects = retrieve_project_by_id(current_user.email)
    print(all_projects)
    num_rows = 3
    start, begin, end = _get_page_limits(page, num_rows, len(all_projects))
    all_projects = all_projects[start:(start+num_rows)]
    return render_template('projects.html', title='All Projects', all_projects=all_projects,begin=begin,
                           end=end, page=page)


def _get_page_limits(page, num_rows, size):
    start = (page - 1) * num_rows
    end = (size // num_rows) if (size % num_rows == 0) else ((size // num_rows)+1)
    begin = (end - 2) if (end == page) else page
    return start, begin, end

@app.route('/del_project/<case>')
def del_project(case):
    remove_project(case)
    return redirect(url_for('projects'))


@app.route('/project/<case>')
@login_required
def project(case):
    users = {"ibobafumba@gmail.com": "Ibo Bafumba", "horimbere86@yahoo.fr": "Briella Horimbere",
             "gabriel@gmail": "Gabriel Bafumba", "jojo@gmail.com": "Johanna Bafumba",
             "blaise.mpinga@ocmgroups.com": "Blaise Mpinga"}
    proj = get_projects_by_project_number(case)
    return render_template('project.html', title='Project', case=case, users=users, proj=proj)


@app.route('/upload/<case>', methods=["GET", "POST"])
def upload(case):
    if request.method == "POST":
        files = request.files.getlist('file')
        for file in files:
            if len(file.filename.strip()) == 0:
                flash(Markup('<strong>Warning!</strong>  No file selected'), 'warning')
                return redirect(url_for('project', case=case))
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('file(s) uploaded successfully', 'success')
        return redirect(url_for('project', case=case))

    else:
        return redirect(url_for('project', case=case))


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
        obj['user_id'] = current_user.email
        obj['client'] = name
        obj['created_at'] = datetime.utcnow()  # TODO change to local time
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


@app.route('/assign', methods=["GET", "POST"])
@login_required
def assign():
    if request.method == "POST":
        email_receiver = request.form['user']
        project_id = request.form['case']
        proj = get_projects_by_project_number(project_id)
        proj['assignee'] = email_receiver
        save_project(proj)
        if send_email(email_receiver, project_id):
            flash(Markup("<strong>Success!</strong> email sent."), 'success')
        else:
            flash(Markup("<strong>Success!</strong> email sent."), 'success')
    return redirect(url_for('project', case=project_id))


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/careers')
def careers():
    return render_template('careers.html')
