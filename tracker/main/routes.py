import os

from flask import Blueprint
from flask import current_app
from flask import render_template, url_for, flash, redirect, request, Markup
from werkzeug.utils import secure_filename
from datetime import datetime

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    d = datetime.now()
    return render_template('home.html', year=d.year)


@main.route('/upload/<case>', methods=["GET", "POST"])
def upload(case):
    if request.method == "POST":
        files = request.files.getlist('file')
        for file in files:
            if len(file.filename.strip()) == 0:
                flash(Markup('<strong>Warning!</strong>  No file selected'), 'warning')
                return redirect(url_for('projects.project', case=case))
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        flash('file(s) uploaded successfully', 'success')
        return redirect(url_for('projects.project', case=case))

    else:
        return redirect(url_for('projects.project', case=case))


@main.route('/account')
def account():
    return render_template('account.html', title='Account')


@main.route('/services')
def services():
    return render_template('services.html')


@main.route('/careers')
def careers():
    return render_template('careers.html')



