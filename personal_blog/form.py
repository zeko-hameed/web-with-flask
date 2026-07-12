
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms_alchemy import QuerySelectField
from wtforms.validators import DataRequired, Length

# حذفنا الاستيراد من هنا ونقلناه لأسفل

def choice_parts():
    # استيراد موضعي (Local Import) لكسر الحلقة المفرغة
    from personal_blog.models import Part
    return Part.query.all()


class add_new_blog_form(FlaskForm):
    title = StringField(label='عنوان المقال', validators=[DataRequired(), Length(min=3)])
    description = TextAreaField(label='وصف المقال', validators=[DataRequired()])
    part = QuerySelectField(label='اختر القسم', query_factory=choice_parts, get_label='name')
    submit = SubmitField(label='رفع المقال')


class add_new_part_form(FlaskForm):
    part = StringField(label='اسم القسم', validators=[DataRequired(), Length(min=3)])
    submit = SubmitField(label='رفع القسم')

class update_new_blog_form(FlaskForm):
    title = StringField(label='عنوان المقال', validators=[DataRequired(), Length(min=3)])
    description = TextAreaField(label='وصف المقال', validators=[DataRequired()])
    part = QuerySelectField(label='اختر القسم', query_factory=choice_parts, get_label='name')
    submit = SubmitField(label='تعديل المقال')