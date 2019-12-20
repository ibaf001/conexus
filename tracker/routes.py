from tracker import app, db, bcrypt
from tracker.models import Employee
from flask import render_template, url_for, flash, redirect, request, abort
from tracker.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from tracker import mysql

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route('/projects')
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
def add_project():
    try:
        if request.method == "POST":
            id = request.form['id']
            jur = request.form['jur']
            county = request.form['county']
            municipality = request.form['municipality']
            assignee = request.form['assignee']
            cur = mysql.connection.cursor()
            cur.execute('''INSERT INTO Project (id, Jur, County, Municipality, Assignee) VALUES 
            ({}, '{}',  '{}' ,'{}', '{}');'''.format(id, jur, county, municipality, assignee))
            mysql.connection.commit()
            return redirect(url_for('projects'))
        else:
            return render_template('add_project.html')
    except:
        abort(404)


@app.route('/del_project/<int:index>')
def del_project(index):
    cur = mysql.connection.cursor()
    cur.execute('''DELETE FROM Project where id = {}'''.format(index))
    mysql.connection.commit()
    return redirect(url_for('projects'))



@app.route('/project/<int:index>')
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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)
