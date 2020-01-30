from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from tracker.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose another one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class ProjectForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired()])
    client = StringField('Client', validators=[DataRequired()])
    county = StringField('County', validators=[DataRequired()])
    municipality = StringField('Municipality', validators=[DataRequired()])

    submit = SubmitField('Add Project')


# forms used for projects
class DukeForm(FlaskForm):
    project_id = StringField('Project #', validators=[DataRequired()], default='DUKE001')
    county = StringField('County', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    #assignee = SelectField(u'assignee', choices=['Ibo', 'Briella'])

    submit = SubmitField('Add')


class IPLForm(FlaskForm):
    project_id = StringField('Project #', validators=[DataRequired()], default='IPL555', render_kw={'readonly': True})
    county = StringField('County', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Add')


class ComcastForm(FlaskForm):
    project_id = StringField('Project #', validators=[DataRequired()])
    county = StringField('County', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    state = StringField('state', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Add')


class CitizenForm(FlaskForm):
    project_id = StringField('Project #', validators=[DataRequired(), Length(min=2, max=18)])
    county = StringField('County', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    sector = StringField('sector', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Add')



