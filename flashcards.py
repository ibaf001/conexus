from flask import (Flask, render_template, abort, jsonify,
                   request, redirect, url_for)
from flask_mysqldb import MySQL
from model import db, Employee

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'johanna14'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'tracker'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route("/")
def welcome():
    return render_template('welcome.html',
                           cards=db)


@app.route("/card/<int:index>")
def card_view(index):
    try:
        card = db[index]
        max_index = len(db) - 1
        return render_template("card.html", card=card, index=index, max_index=max_index)
    except IndexError:
        abort(404)


@app.route("/api/card/")
def api_card_list():
    return jsonify(db)


@app.route("/api/card/<int:index>")
def api_card_detail(index):
    try:
        return db[index]
    except IndexError:
        abort(404)


@app.route('/add_card', methods=["GET", "POST"])
def add_card():
    if request.method == "POST":
        card = {"question": request.form['question'],
                "answer": request.form['answer']}
        db.append(card)
        return redirect(url_for('card_view', index=len(db) - 1))
    else:
        return render_template("add_card.html")


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

    return render_template('projects.html', employees=employees)


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
            ({}, '{}',  '{}' ,'{}', '{}');'''.format(id,jur,county,municipality,assignee))
            mysql.connection.commit()
            return redirect(url_for('projects'))
        else:
            print('sellltart bafumba')
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
    return render_template('project.html', emp=emp)


@app.route('/remove_project/<int:index>')
def remove_project(index):
    return 'project with index {} removed'.format(index)


def save_db():
    pass


@app.route('/remove_card/<int:index>', methods=["GET", "POST"])
def remove_card(index):
    try:
        if request.method == "POST":
            del db[index]
            save_db()
            return redirect(url_for('welcome'))
        else:
            return render_template("remove_card.html", card=db[index])
    except IndexError:
        abort(404)
