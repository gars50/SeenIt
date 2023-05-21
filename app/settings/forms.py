from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models.user import User

class EditUserForm(FlaskForm):
    email = StringField('Email Address')
    alias = StringField('Alias')
    admin = BooleanField('Admin')
    submit = SubmitField('Save')

class ConnectionForm(FlaskForm):
    host = StringField('Hostname', validators=[DataRequired()])
    port = StringField('Port', validators=[DataRequired()])
    apiKey = StringField('API Key', validators=[DataRequired()])
    save = SubmitField('Save')