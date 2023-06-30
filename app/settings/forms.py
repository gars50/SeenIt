from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, validators, ValidationError, SelectField
from app.models.user import User


class EditUserForm(FlaskForm):
    email = StringField('Email Address')
    alias = StringField('Alias')
    admin = BooleanField('Admin')
    submit = SubmitField('Save')

class AddUserForm(FlaskForm):
    email = StringField('Email Address')
    alias = StringField('Alias')
    admin = BooleanField('Admin')
    submit = SubmitField('Save')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('An account with that email address is already present.')
        
class EditAppSettings(FlaskForm):
    delayNumber = IntegerField(validators=[validators.NumberRange(min=0)])
    delayUnit = SelectField(u'Unit', choices=[("minutes","minutes"), ("hours","hours"), ("days","days"), ("weeks","weeks")])
    appName = StringField('Application Name')
    radarrHost = StringField()
    radarrPort = IntegerField(validators=[validators.Optional()])
    radarrApiKey = StringField()
    sonarrHost = StringField()
    sonarrPort = IntegerField(validators=[validators.Optional()])
    sonarrApiKey = StringField()
    ombiHost = StringField()
    ombiPort = IntegerField(validators=[validators.Optional()])
    ombiApiKey = StringField()
    submit = SubmitField('Save')