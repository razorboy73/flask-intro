__author__ = 'workhorse'

from sqlalchemy import ForeignKey, func # pragma: no cover
from sqlalchemy.orm import relationship, backref # pragma: no cover
from project import db # pragma: no cover
from project import bcrypt # pragma: no cover
import datetime



class BlogPost(db.Model):
    __tablename__='posts'
    id = db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String(128), nullable=False)
    description = db.Column(db.String, nullable=False)
    image_path = db.Column(db.String(255))
    user_id = db.Column(db.Integer, ForeignKey('users.id'))

    def __init__(self, title, description, image_path, user_id):
        self.title = title
        self.description =description
        self.image_path=image_path
        self.user_id = user_id

    def __repr__(self):
        return "<title {}>".format(self.title)

class Instructor(db.Model):
    __tablename__='instructors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.Integer, nullable=True)
    hired_on = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=False)
    course_id = db.Column(db.Integer, ForeignKey('courses.id'))

    def __init__(self, first_name, last_name, email, phone, hired_on, active, course_id):

        self.first_name= first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.hired_on = hired_on
        self.active = active
        self.course_id = course_id

        def __repr__(self):
            return "<firstName: {} lastName:{}>".format(self.title)


class Student(db.Model):
    __tablename__='students'

    id = db.Column(db.Integer, primary_key=True)
    date_enrolled = db.Column(db.DateTime, nullable=False, default=func.now())
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    parent_first_name = db.Column(db.String, nullable=False)
    parent_last_name = db.Column(db.String, nullable=False)
    parent_email = db.Column(db.String, nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    second_parent_first_name = db.Column(db.String, nullable=True)
    second_parent_last_name = db.Column(db.String, nullable=True)
    second_parent_email = db.Column(db.String, nullable=True)
    second_parent_phone = db.Column(db.Integer, nullable=True)
    medical_issues = db.Column(db.String, nullable=True)
    custody_issues = db.Column(db.String, nullable=True)
    release_people = db.Column(db.String, nullable=True)
    referral_source = db.Column(db.String, nullable=True)
    student_email = db.Column(db.String, nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=False)
    fully_paid = db.Column(db.Boolean, nullable=False, default=False)
    amount_paid = db.Column(db.Integer, nullable=True)
    #course_id = db.Column(db.Integer, ForeignKey('courses.id'))

    def __init__(self, first_name, last_name, email, phone, hired_on, active, course_id):

        self.first_name= first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.hired_on = hired_on
        self.active = active
        self.course_id = course_id

        def __repr__(self):
            return "<firstName: {} lastName:{}>".format(self.title)



class Course(db.Model):
    __tablename__='courses'
    id = db.Column(db.Integer, primary_key=True)
    course_title =db.Column(db.String(128), nullable=False)
    course_description = db.Column(db.String, nullable=True)
    course_location = db.Column(db.String, nullable=True)
    course_start_date = db.Column(db.DateTime, nullable=True)
    course_end_date = db.Column(db.DateTime, nullable=True )
    course_duration = db.Column(db.Float, nullable=True )
    class_start_time = db.Column(db.Time, nullable=True)
    class_end_time = db.Column(db.Time, nullable=True)
    class_duration = db.Column(db.Time, nullable=True)
    course_price = db.Column(db.Float, nullable=True )
    course_num_students = db.Column(db.Integer, nullable=True )
    course_instructor = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    instructor = relationship("Instructor", backref="instructors",  lazy="dynamic")


    def __init__(self, course_title,  user_id, course_description=None, course_location=None, course_start_date=None,
                 course_end_date=None,course_duration=None, class_start_time=None, class_end_time=None, course_price=None,
                 course_num_students=None, course_instructor=None ):

        self.course_title = course_title
        self.course_description =course_description
        self.course_location = course_location
        self.course_start_date = course_start_date
        self.course_end_date = course_end_date
        self.course_duration = course_duration
        self.class_start_time = class_start_time
        self.class_end_time = class_end_time
        self.course_price = course_price
        self.course_num_students = course_num_students
        self.course_instructor = course_instructor
        self.user_id = user_id

    def __repr__(self):
        return "<course title {}>".format(self.course_title)

class User(db.Model):
    __tablename__ ="users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    posts = relationship("BlogPost", backref="author",  lazy="dynamic")
    course = relationship("Course", backref="course",  lazy="dynamic")

    def __init__(self, username, email, password,admin=False,confirmed=False,
                 paid=False, confirmed_on=None):
        self.name = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def is_admin(self):
        return self.admin



    def __repr__(self):
        return "<name - {}>".format(self.name)




