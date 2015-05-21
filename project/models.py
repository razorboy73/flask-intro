__author__ = 'workhorse'

from sqlalchemy import ForeignKey # pragma: no cover
from sqlalchemy.orm import relationship # pragma: no cover
from project import db # pragma: no cover
from project import bcrypt # pragma: no cover



class BlogPost(db.Model):
    __tablename__='posts'
    id = db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String(128), nullable=False)
    description = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))

    def __init__(self, title, description, user_id):
        self.title = title
        self.description =description
        self.user_id = user_id

    def __repr__(self):
        return "<title {}>".format(self.title)


class User(db.Model):
    __tablename__ ="users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    posts = relationship("BlogPost", backref="author",  lazy="dynamic")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


    def __repr__(self):
        return "<name - {}>".format(self.name)




