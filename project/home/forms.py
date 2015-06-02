__author__ = 'workhorse'

from flask_wtf import Form
from wtforms import StringField, FileField, DateTimeField, IntegerField, BooleanField, FloatField
from wtforms.validators import DataRequired, Length

class MessageForm(Form):
    title = StringField("Title", validators=[DataRequired()])
    description = StringField(
        "Description", validators=[DataRequired(), Length(max=140)]
    )
    image = FileField("Product Image")

class CourseForm(Form):
    course_name = StringField("Title", validators=[DataRequired()])
    course_description = StringField("Course Description", validators=[DataRequired()])
    course_location = StringField("Course Location", validators=[DataRequired()])
    start_date = DateTimeField("Start Date", validators=[DataRequired()])
    end_date = DateTimeField("End Date", validators=[DataRequired()])
    start_time = DateTimeField("Start Time", validators=[DataRequired()])
    end_time = DateTimeField("End Time", validators=[DataRequired()])
    max_number_students = IntegerField("Max Students", validators=[DataRequired()])
    spaces_left = IntegerField("Spaces Left")
    is_active = BooleanField("Is Active")
    price = FloatField("Price in Dollars")
    age_range = StringField("Age range", validators=[DataRequired()])
    image_path = FileField("Product Image")
