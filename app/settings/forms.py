from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, validators, ValidationError
from app.models.user import User


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

class AddUserForm(FlaskForm):
    email = StringField('Email Address')
    alias = StringField('Alias')
    admin = BooleanField('Admin')
    submit = SubmitField('Save')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('An account with that email address is already present.')