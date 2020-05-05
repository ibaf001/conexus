import os
from datetime import datetime

from flask import Blueprint
from flask import current_app
from flask import render_template, url_for, flash, redirect, request, Markup
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email

from tracker.projects import utils

main = Blueprint('main', __name__)


class ContactForm(FlaskForm):
    name = StringField("Name")
    email = EmailField('Email', [DataRequired(), Email()])
    subject = StringField("Subject")
    message = TextAreaField("Message", validators=[DataRequired("Please enter a message")])
    submit = SubmitField("Send")


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


@main.route('/contactus', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        if utils.send_message(form):
            flash('Message Sent', 'success')
    if form.errors:
        flash(f'{form.errors}', 'danger')
    return render_template('contact.html', form=form)
