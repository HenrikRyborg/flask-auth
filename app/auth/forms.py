from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import account

class registerAccountForm(FlaskForm):
    accountName = StringField('Account Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirmPassword')])
    confirmPassword = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validateAccount(self, field):
        if account.query.filter_by(name=field.data).first():
            raise ValidationError('Account is already in use.')

class setPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirmPassword')])
    confirmPassword = PasswordField('Confirm Password')
    submit = SubmitField('Register')

class loginForm(FlaskForm):
    accountName = StringField('Account Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')