from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, validators, ValidationError, SelectField, DateTimeLocalField
from wtforms.validators import DataRequired
from app.models import User, Role


class EditUserForm(FlaskForm):
    email = StringField('Email Address')
    alias = StringField('Alias', validators=[DataRequired()])
    #Need to make this better to go according to Role class
    role = SelectField('Role', choices=["User", "Power User", "Administrator"])
    submit = SubmitField('Save')

class AddUserForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    alias = StringField('Alias', validators=[DataRequired()])
    role = SelectField('Role', choices=["User", "Power User", "Administrator"])
    submit = SubmitField('Save')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('An account with that email address is already present.')
        
class EditAppSettings(FlaskForm):
    expiry_time_number = IntegerField("After how much time should an abandoned media be marked expired", validators=[validators.NumberRange(min=0)])
    expiry_time_unit = SelectField('Unit', choices=["minutes","hours","days","weeks","months"])
    next_delete = DateTimeLocalField('When should the next check for deletion of expired media be', format='%Y-%m-%dT%H:%M')
    deletion_time_number = IntegerField('Reoccurs every', validators=[validators.NumberRange(min=0)])
    deletion_time_unit = SelectField('Unit', choices=["hours","days","weeks","months",])
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
    safe_mode = BooleanField('Safe Mode. Allows to delete objects only from the SeenIt database, and not from Ombi/Radarr/Sonarr')
    submit = SubmitField('Save')