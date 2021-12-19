from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flaskblog.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    image = FileField('image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. please choose another')


class AsosRegistrationForm(RegistrationForm):
    name = StringField('שם העמותה', validators=[DataRequired(), Length(min=2, max=20)])
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=20)])

    def validate_address(self, address):
        user = User.query.filter_by(address=address.data).first()
        if user:
            raise ValidationError('That address is taken. please choose another')


class BusRegistrationForm(RegistrationForm):
    name = StringField('שם העסק', validators=[DataRequired(), Length(min=2, max=20)])
    bus_id = IntegerField('bus id', validators=[DataRequired()])

    def validate_bus_id(self, bus_id):
        user = User.query.filter_by(bus_id=bus_id.data).first()
        if user:
            raise ValidationError('That bus id is taken. please choose another')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=2, max=1000)])
    image = FileField('image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    type = SelectField('Type',  validators=[DataRequired()], choices=['adopt', 'foster'])
    price = IntegerField('Price')
    submit = SubmitField('Save')

class UpdateAccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    image = FileField('image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data!=current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. please choose another')
