from datetime import datetime

import pandas as pd
from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, Markup
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, validators
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from werkzeug.utils import escape, unescape
from tracker.projects import utils

projects = Blueprint('projects', __name__)

num_rows = 5


@projects.route('/projects', defaults={'page': 1})
@projects.route('/projects/<int:page>')
@login_required
def get_projects(page):
    try:
        all_projects = utils.get_all_projects()
        start, begin, end = _get_page_limits(page, num_rows, len(all_projects))
        all_projects = all_projects[start:(start + num_rows)]
        pcount = utils.get_projects_count()
        return render_template('projects.html', title='All Projects', all_projects=all_projects,
                               end=end, page=page, pcount=pcount, limits=_get_pagination_range(page, end),
                               client_name=None)
    except:
        return  render_template('errors/500.html')


def _get_pagination_range(page, end):
    limits = []
    if page > 1:
        limits.append(page - 1)
    limits.append(page)
    if page < end:
        limits.append(page + 1)
    return limits


def _get_page_limits(page, num_rows, size):
    start = (page - 1) * num_rows
    end = (size // num_rows) if (size % num_rows == 0) else ((size // num_rows) + 1)
    begin = (end - 2) if (end == page) else page
    return start, begin, end


@projects.route('/del_project/<case>')
@login_required
def del_project(case):
    utils.remove_project(case)
    return redirect(url_for('projects.get_projects'))


@projects.route('/project/<case>')
@login_required
def project(case):
    users = {"ibobafumba@gmail.com": "Ibo Bafumba", "horimbere86@yahoo.fr": "Briella Horimbere",
             "gabriel@gmail": "Gabriel Bafumba", "jojo@gmail.com": "Johanna Bafumba",
             "blaise.mpinga@ocmgroups.com": "Blaise Mpinga"}
    proj = utils.get_projects_by_project_number(case)
    proj['created at'] = datetime.strftime(proj['created at'], '%Y-%m-%d')
    return render_template('project.html', title='Project', case=case, users=users, proj=proj)


# todo reanalyze this method ...
def escape_fields(d):
    for k, v in d.items():
        d[k] = unescape(v)
    return d


@projects.route("/add_client/<name>", methods=["GET", "POST"])
@login_required
def add_client(name):
    if request.method == "POST":
        files = request.files.getlist('file')
        for file in files:
            if len(file.filename.strip()) == 0:
                flash(Markup('<strong>Warning!</strong>  No file selected'), 'warning')
                break
            if not utils.is_csv_file(file.filename):
                flash('Please select a .csv file', 'warning')
                break
            try:
                clients = utils.get_clients()
                fname = utils.get_csv_filename(file.filename)
                if fname in clients:
                    # todo delete client because exists
                    pass
                df = pd.read_csv(file)
                client_obj = {'_id': fname, 'fields': utils.create_fields(df)}
                utils.save_client(client_obj)
                flash(f'client: {file.filename} was uploaded successfully', 'success')
            except Exception as e:
                flash(Markup(f'<strong>Danger!</strong>  An exception occurred: {e}'), 'danger')
    form = build_form(name)
    clients = utils.get_clients()
    return redirect(url_for('projects.add_project', name=name, form=form, clients=clients, selected=name))


@projects.route('/assign', methods=["GET", "POST"])
@login_required
def assign():
    if request.method == "POST":
        email_receiver = request.form['user']
        project_id = request.form['case']
        proj = utils.get_projects_by_project_number(project_id)
        proj['assignee'] = email_receiver
        utils.save_project(proj)
        if utils.send_email(email_receiver, project_id):
            flash(Markup("<strong>Success!</strong> email sent."), 'success')
        else:
            flash(Markup("<strong>Success!</strong> email sent."), 'success')
    return redirect(url_for('projects.project', case=project_id))


@projects.route("/add_project/", defaults={'name': 'Duke'}, methods=["GET", "POST"])
@projects.route("/add_project/<name>", methods=["GET", "POST"])
def add_project(name):
    clients = utils.get_clients()
    form = build_form(name)()
    if form and form.validate_on_submit():
        pj = {}
        for field in form:
            if field.name not in ('csrf_token', 'submit'):
                pj[field.name] = escape(str(field.data))
        if len(pj) != 0:
            pj['user_id'] = current_user.email
            pj['client'] = name
            pj['created at'] = datetime.now()  # TODO change to local time
            utils.save_project(pj)
            flash('project created successfully', 'success')

        return redirect(url_for('projects.add_project', name=name, form=form, clients=clients, selected=name))
    return render_template('add_project.html', clients=clients, form=form, selected=name)


name_map = dict()  # todo need to fix this .. put under __init__.py ?? global space


def build_form(name):
    if name not in name_map:
        record = utils.get_client_by_id(name)['fields']
        A = type(name, (FlaskForm,), {})
        for key, value in record.items():
            setattr(A, key, get_client_form(value))
        setattr(A, 'Due Date', DateField('Due Date', format='%Y-%m-%d', validators=(validators.Optional(),)))
        setattr(A, 'submit', SubmitField('submit'))
        name_map[name] = A
        return A
    return name_map.get(name)


@projects.route('/projects_by_client/<client_name>', defaults={'page': 1})
@projects.route('/projects_by_client/<int:page>/<client_name>')
@login_required
def projects_by_client(client_name, page):
    all_projects = utils.get_projects_for(client_name)
    start, begin, end = _get_page_limits(page, num_rows, len(all_projects))
    all_projects = all_projects[start:(start + num_rows)]
    pcount = utils.get_projects_count()
    return render_template('projects.html', title='All Projects', all_projects=all_projects,
                           end=end, page=page, pcount=pcount, client_name=client_name,
                           limits=_get_pagination_range(page, end))


@projects.route('/forward/<int:page>', defaults={'client_name': None})
@projects.route('/forward/<int:page>/<client_name>')
@login_required
def forward(client_name, page):
    if client_name is None or client_name.strip() == '':
        return redirect(url_for('projects.get_projects', page=page))
    return redirect(url_for('projects.projects_by_client', client_name=client_name, page=page))


@projects.route('/update_project/<project_number>', methods=["GET", "POST"])
@login_required
def update_project(project_number):
    if request.method == 'POST':
        form = request.form
        obj = dict()
        for field in form:
            if field not in ('submit', 'csrf_token'):
                obj[field] = escape(form.get(field))
        utils.update_project(obj, project_number)
        flash('project updated successfully', 'success')
        return redirect(url_for('projects.update_project', form=form, project_number=project_number))

    proj = utils.get_projects_by_project_number(project_number)
    form = build_form(proj['client'])()
    for field in form:
        if field.name not in ('submit', 'csrf_token', 'DueDate'):
            field.data = unescape(proj[field.name])
        if field.name == 'submit':
            field.label.text = 'update'
        if field.name == 'Due Date':
            if proj[field.name] == 'None':
                field.data = ''
            else:
                field.data = datetime.strptime(proj[field.name], '%Y-%m-%d')

    return render_template('update_project.html', form=form, client=proj['client'], project_number=project_number)


@projects.route('/search_project', methods=["POST"])
@login_required
def search_project():
    project_number = request.form.get('project_number')
    if len(project_number.strip()) == 0:
        return redirect(url_for('projects.get_projects'))
    all_projects = utils.search_project(project_number)
    start, begin, end = _get_page_limits(1, num_rows,
                                         len(all_projects))  # todo change number page (was replace by 1
    all_projects = all_projects[start:(start + num_rows)]
    pcount = utils.get_projects_count()
    return render_template('projects.html', search=True, all_projects=all_projects, pcount=pcount, title='Search')


def is_required(data):
    v = []
    if data:
        v.append(DataRequired())
    return v


def build_choices(entries):
    d = entries.split('-')
    dd = []
    for option in d:
        dd.append((option, option))
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
