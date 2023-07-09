from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, validators, ValidationError, SelectField, DateTimeField
from app.models import User


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
    expiryTimeNumber = IntegerField("After how much time should an abandonned media be marked expired", validators=[validators.NumberRange(min=0)])
    expiryTimeUnit = SelectField('Unit', choices=[("minutes","minutes"), ("hours","hours"), ("days","days"), ("weeks","weeks"), ("months","months")])
    nextDelete = DateTimeField('When should the next check for deletion of expired media be', format='%Y-%m-%d %H:%M:%S')
    deletionTimeNumber = IntegerField('How often should that be checked', validators=[validators.NumberRange(min=0)])
    deletionTimeUnit = SelectField('Unit', choices=[("minutes","minutes"), ("hours","hours"), ("days","days"), ("weeks","weeks"), ("months","months")])
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