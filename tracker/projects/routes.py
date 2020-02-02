from datetime import datetime

from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, Markup
from flask_login import current_user, login_required
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired

from tracker.projects.forms import (DukeForm, IPLForm, ComcastForm, CitizenForm, ClientForm)
from tracker.projects.utils import *

projects = Blueprint('projects', __name__)


@projects.route('/projects', defaults={'page': 1})
@projects.route('/projects/<int:page>')
@login_required
def get_projects(page):
    all_projects = retrieve_project_by_id(current_user.email)
    print(all_projects)
    num_rows = 3
    start, begin, end = _get_page_limits(page, num_rows, len(all_projects))
    all_projects = all_projects[start:(start + num_rows)]
    return render_template('projects.html', title='All Projects', all_projects=all_projects, begin=begin,
                           end=end, page=page)


def _get_page_limits(page, num_rows, size):
    start = (page - 1) * num_rows
    end = (size // num_rows) if (size % num_rows == 0) else ((size // num_rows) + 1)
    begin = (end - 2) if (end == page) else page
    return start, begin, end


@projects.route('/del_project/<case>')
@login_required
def del_project(case):
    remove_project(case)
    return redirect(url_for('projects.get_projects'))


@projects.route('/project/<case>')
@login_required
def project(case):
    users = {"ibobafumba@gmail.com": "Ibo Bafumba", "horimbere86@yahoo.fr": "Briella Horimbere",
             "gabriel@gmail": "Gabriel Bafumba", "jojo@gmail.com": "Johanna Bafumba",
             "blaise.mpinga@ocmgroups.com": "Blaise Mpinga"}
    proj = get_projects_by_project_number(case)
    return render_template('project.html', title='Project', case=case, users=users, proj=proj)


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


@projects.route("/add_project/", defaults={'name': 'Duke'}, methods=["GET", "POST"])
@projects.route("/add_project/<name>", methods=["GET", "POST"])
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


@projects.route('/assign', methods=["GET", "POST"])
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
    return redirect(url_for('projects.project', case=project_id))


@projects.route('/example', methods=["GET", "POST"])
def example():
    clients = ['Duke', 'IPL', 'Comcast', 'Citizen']
    record = {'project': ['stringfield','project', False, ''],
              'county': ['stringfield', 'county', True, ''],
              'status': ['selectfield','status', True,'started-In progress-completed'],
              'City': ['stringfield','city', True, 'Indianapolis'],
              'Notes': ['textareafield','notes', False,'']}
    form = ClientForm()
    for key, value in record.items():
        setattr(ClientForm, key, get_client_form(value))
    setattr(ClientForm, 'submit', SubmitField('submit'))
    if form.validate_on_submit():
        # print(dict(form.status.choices).get(form.status.data))  todo how to get value for selection
        return 'form is submitted- county is: ' + str(form.county.data)
    return render_template('example.html', clients=clients, form=form)


def is_required(data):
    v = []
    if data:
        v.append(DataRequired())
    return v


def build_choices(entries):
    d = entries.split('-')
    dd = []
    for option in d:
        dd.append((''.join(option.split()), option))
    return dd


def get_client_form(data):
    if data[0].lower() == 'stringfield':
        return StringField(data[1], validators=is_required(data[2]), default=data[3])
    elif data[0].lower() == 'textareafield':
        return TextAreaField(data[1])
    elif data[0].lower() == 'selectfield':
        return SelectField(data[1], choices=build_choices(data[3]))
    else:
        return StringField(data[1], validators=is_required(data[2]), default=data[3])



