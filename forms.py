from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import Length, DataRequired, EqualTo, Regexp, Email


class CryptoForm(FlaskForm):
    crypto = StringField('CryptoCurrency', validators=[DataRequired(), Length(max=5)])
    starter_price = FloatField('Starting price')
    target_price = FloatField('Target price')
    date_to_target = DateField('Date to target price', format='%Y-%m-%d')
    submit = SubmitField('Post')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'No special characters allowed.')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'No special characters allowed.')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')