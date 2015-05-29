__author__ = 'workhorse'

from sqlalchemy import ForeignKey, func # pragma: no cover
from sqlalchemy.orm import relationship # pragma: no cover
from project import db # pragma: no cover
from project import bcrypt # pragma: no cover
import datetime

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String, nullable=True)
    course_location = db.Column(db.String, nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    max_number_students = db.Column(db.Integer, default=8)
    spaces_left = db.Column(db.Integer, default=5)
    is_active = db.Column(db.Boolean, default=True)
    price = db.Column(db.Float, nullable=True)



    def __init__(self, course_name=None, course_description=None, course_location=None,start_date=None,end_date=None,
                start_time=None,end_time=None,max_number_students=None,spaces_left=None,is_active=None, price=None):
        self.course_name = course_name
        self.course_description=course_description
        self.course_location = course_location
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.max_number_students = max_number_students
        self.spaces_left = spaces_left
        self.is_active = is_active
        self.price = price


    def __repr__(self):
        return "<course name {}>".format(self.course_name)


class Purchase(db.Model):
    __tablename__ = 'purchases'
    uuid = db.Column(db.String, primary_key=True)
    email = db.Column(db.String)
    product_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    payment_method = db.Column(db.String, nullable=True, default="Credit Card")
    notes = db.Column(db.String, nullable=True)
    date_purchased = db.Column(db.DateTime, nullable=False, default=func.now())
    product = db.relationship(Course)

    def __init__(self, uuid,email=None, product_id=None, product=None,payment_method=None, notes=None, date_purchased=None):
        self.uuid=uuid
        self.email=email
        self.product_id=product_id
        self.product = product
        self.payment_method=payment_method
        self.notes=notes
        self.date_purchased=date_purchased


    def __repr__(self):
        return "<product_id {}>".format(self.product_id)

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




