from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models.user import User

class UserForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    admin = BooleanField('Admin')
    submit = SubmitField('Save')
    delete = SubmitField('Delete')
        

class ConnectionForm(FlaskForm):
    host = StringField('Hostname', validators=[DataRequired()])
    port = StringField('Port', validators=[DataRequired()])
    apiKey = StringField('API Key', validators=[DataRequired()])
    test = SubmitField('Test')
    save = SubmitField('Save')