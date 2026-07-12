from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, EmailField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, NumberRange, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user


from car_app.models import User


class new_car(FlaskForm):
    name = StringField(label="name", validators=[DataRequired(), Length(min=3, max=15)])
    discrption = StringField(label="discrption", validators=[DataRequired(), Length(min=5, max=50)])
    photo = FileField(label="upload your car", validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
    price = IntegerField(label='price', validators=[DataRequired(), NumberRange(min=9)])
    submit = SubmitField(label="upload")


class new_news(FlaskForm):
    title = StringField(label="title", validators=[DataRequired(), Length(min=3, max=50)])
    description = StringField(label="description", validators=[DataRequired(), Length(min=5, max=250)])
    photo = FileField(label="upload news photo", validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
    submit = SubmitField(label="upload")


class new_account(FlaskForm):
    name = StringField(label="username", validators=[DataRequired(), Length(min=2)])
    email = EmailField(label="email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=6)])
    Convirt_password = PasswordField(label="Convirt-Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Sign up')

    def validate_name(self, name):
        user = User.query.filter_by(username=name.data).first()
        if user:
            raise ValidationError('username already exist')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('username already exist')


class login_account(FlaskForm):
    email = EmailField(label="email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField(label='Sign up')


class update_profile(FlaskForm):
    username = StringField(label="username", validators=[DataRequired(), Length(min=3, max=20)])
    email = EmailField(label="email", validators=[DataRequired(), Email()])
    profile_pitcir = FileField(label="updata your profile", validators=[FileAllowed(['png', 'jpg'], message='only png and jpg')])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField(label="up data")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('username already exist')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('email already exist')
            



