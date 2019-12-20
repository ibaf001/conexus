from flask import render_template, url_for, flash, redirect, request, abort

from tracker import app,  db, bcrypt
from tracker import mysql
from tracker.forms import RegistrationForm, LoginForm, ProjectForm
from tracker.models import Employee, User, Project
from flask_login import login_user, current_user, logout_user, login_required



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route('/projects')
@login_required
def projects():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM Project''')

    employees = []
    num_rows = cur.rowcount
    for x in range(0, num_rows):
        row = cur.fetchone()
        emp = Employee(row['id'], row['Jur'], row['Assignee'])
        employees.append(emp)

    return render_template('projects.html', title='All Projects', employees=employees)


@app.route('/add_project', methods=["GET", "POST"])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        flash('You project has been created', 'success')
        return redirect(url_for('home'))
    return render_template('add_project.html', title ='New Project', form=form)


@app.route('/del_project/<int:index>')
def del_project(index):
    cur = mysql.connection.cursor()
    cur.execute('''DELETE FROM Project where id = {}'''.format(index))
    mysql.connection.commit()
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
        user =User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
def account():
    return render_template('account.html', title='Account')

