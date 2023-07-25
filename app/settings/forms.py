from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, validators, ValidationError, SelectField, DateTimeLocalField
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
    expiry_time_number = IntegerField("After how much time should an abandonned media be marked expired", validators=[validators.NumberRange(min=0)])
    expiry_time_unit = SelectField('Unit', choices=[("minutes","minutes"), ("hours","hours"), ("days","days"), ("weeks","weeks"), ("months","months")])
    next_delete = DateTimeLocalField('When should the next check for deletion of expired media be', format='%Y-%m-%dT%H:%M')
    deletion_time_number = IntegerField('Reoccurs every', validators=[validators.NumberRange(min=0)])
    deletion_time_unit = SelectField('Unit', choices=[("hours","hours"), ("days","days"), ("weeks","weeks"), ("months","months")])
    app_name = StringField('Application Name')
    radarr_host = StringField()
    radarr_port = IntegerField(validators=[validators.Optional()])
    radarr_api_key = StringField()
    sonarr_host = StringField()
    sonarr_port = IntegerField(validators=[validators.Optional()])
    sonarr_api_key = StringField()
    ombi_host = StringField()
    ombi_port = IntegerField(validators=[validators.Optional()])
    ombi_api_key = StringField()
    submit = SubmitField('Save')