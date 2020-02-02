from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class ClientForm(FlaskForm):
    pass


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
    language = SelectField('Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])

    notes = TextAreaField('Notes')
    # assignee = SelectField(u'assignee', choices=['Ibo', 'Briella'])

    submit = SubmitField('Add')


class IPLForm(FlaskForm):
    project_id = StringField('Project #', validators=[DataRequired()], default='IPL555', render_kw={'readonly': True})
    county = StringField('County', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[DataRequired()])
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
