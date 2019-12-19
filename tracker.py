from flask import (Flask, render_template, abort, jsonify,flash,
                   request, redirect, url_for)
from flask_mysqldb import MySQL
from model import db, Employee
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '850b0126f8f89a2637d77e2d29086569'


app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'johanna14'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'tracker'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route("/")
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
