from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class Do_list(FlaskForm):
    title = StringField(label="المهمة", validators=[DataRequired(), Length(min=3)])
    descrption = TextAreaField(label="وصف المهمة", validators=[DataRequired()])
    submit = SubmitField(label="رفع المهمة")




class update_list(FlaskForm):
    title = StringField(label="المهمة", validators=[DataRequired(), Length(min=3)])
    descrption = TextAreaField(label="وصف المهمة", validators=[DataRequired()])
    submit = SubmitField(label="رفع المهمة")


