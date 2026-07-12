from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, TextAreaField, FloatField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from inventory_app.models import Users



class create_account_form(FlaskForm):
    username = StringField(label='اسم المستخدم', validators=[DataRequired(), Length(min=2)])
    email = EmailField(label='البريد الإلكتروني', validators=[DataRequired(), Email()])
    password = PasswordField(label='كلمة المرور', validators=[DataRequired(), Length(min=8)])
    confirt_password = PasswordField(label='إعادة كلمة المرور', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='إنشاء حساب')

    def validate_username(self, username):
        user = Users.query.filter_by(name=username.data).first()
        if user:
            raise ValidationError('الإسم مستخدم مسبقاً')
    
    def validate_email(self, email):
        email = Users.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('البريد مستخدم مسبقاً')


class profile_form(FlaskForm):
    username = StringField(label='اسم المستخدم', validators=[DataRequired(), Length(min=2)])
    email = EmailField(label='البريد الإلكتروني', validators=[DataRequired(), Email()])
    image_url = FileField(label='صورة المستخدم', validators=[FileAllowed(['png', 'jpg'])])
    submit = SubmitField(label='تعديل')

    def validate_username(self, username):
        if username.data != current_user.name:
            user = Users.query.filter_by(name=username.data).first()
            if user:
                raise ValidationError('الإسم مستخدم مسبقاً')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            email = Users.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('البريد مستخدم مسبقاً')


class login_account_form(FlaskForm):
    email = EmailField(label='البريد الإلكتروني', validators=[DataRequired(), Email()])
    password = PasswordField(label='كلمة المرور', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label='تسجيل الدخول')

class add_item_Form(FlaskForm):
    name = StringField(label='اسم المنتج', validators=[DataRequired(), Length(min=3)])
    description = TextAreaField(label='وصف المنتج', validators=[DataRequired()])
    image_url = FileField(label='صورة للمنتج', validators=[FileAllowed(['png','jpg'])])
    price = FloatField(label='سعر المنتج', validators=[DataRequired()])
    submit = SubmitField(label='رفع المنتج')


class update_item_Form(FlaskForm):
    name = StringField(label='اسم المنتج', validators=[DataRequired(), Length(min=3)])
    description = TextAreaField(label='وصف المنتج', validators=[DataRequired()])
    image_url = FileField(label='صورة للمنتج', validators=[FileAllowed(['png','jpg'])])
    price = FloatField(label='سعر المنتج', validators=[DataRequired()])
    submit = SubmitField(label='تعديل المنتج')


