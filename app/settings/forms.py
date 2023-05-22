from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, validators


class EditUserForm(FlaskForm):
    email = StringField('Email Address')
    alias = StringField('Alias')
    admin = BooleanField('Admin')
    submit = SubmitField('Save')

class EditConnectionsForm(FlaskForm):
    hostRadarr = StringField()
    portRadarr = IntegerField(validators=[validators.Optional()])
    apiKeyRadarr = StringField()
    hostSonarr = StringField()
    portSonarr = IntegerField(validators=[validators.Optional()])
    apiKeySonarr = StringField()
    hostOmbi = StringField()
    portOmbi = IntegerField(validators=[validators.Optional()])
    apiKeyOmbi = StringField()
    submit = SubmitField('Save')