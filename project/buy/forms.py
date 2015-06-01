__author__ = 'workhorse'

from flask_wtf import Form

from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Email
from project.models import Course

def select_group():
        return Course.query.all()


class EnrollmentForm(Form):

    email = StringField(
        "email",
        validators=[DataRequired(), Email(message = None),Length(min=3, max=40)]
    )
    product= QuerySelectField(query_factory=select_group)
    payment_method = StringField('Payment', validators=[DataRequired()])
    notes = StringField('Notes', validators=[DataRequired()])

