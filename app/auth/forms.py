from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import account

class registerAccountForm(FlaskForm):
    accountName = StringField('Account Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirmPassword')])
    confirmPassword = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_password(self, field):
        if len(field.data) < 6:
            raise ValidationError('password must be at least 6 characters')

    def validate_accountName(self, field):
        if len(field.data) > 20:
            raise ValidationError('Name must be less than 20 characters')
        if account.query.filter_by(name=field.data).first():
            raise ValidationError('Account is already in use.')

class setPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirmPassword')])
    confirmPassword = PasswordField('Confirm Password')
    submit = SubmitField('Register')

class inviteUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Invite')

class assignRolesToUserForm(FlaskForm):
    user = SelectField('User', choices=[], validators=[DataRequired()])
    role = SelectMultipleField('Role', choices=[], validators=[DataRequired()])
    submit = SubmitField('Assign')

class assignUsersToRoleForm(FlaskForm):
    role = SelectField('Role', choices=[], validators=[DataRequired()])
    users = SelectMultipleField('Users', choices=[], validators=[DataRequired()])
    submit = SubmitField('Assign')

class assignGroupsToUserForm(FlaskForm):
    user = SelectField('User', choices=[], validators=[DataRequired()])
    group = SelectMultipleField('Group', choices=[], validators=[DataRequired()])
    submit = SubmitField('Assign')

class assignUsersToGroupForm(FlaskForm):
    group = SelectField('Group', choices=[], validators=[DataRequired()])
    users = SelectMultipleField('Users', choices=[], validators=[DataRequired()])
    submit = SubmitField('Assign')

class loginForm(FlaskForm):
    accountName = StringField('Account Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')