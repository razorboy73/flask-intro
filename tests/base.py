__author__ = 'workhorse'
from flask.ext.testing import TestCase
from project import db
from flask import current_app
from project.models import BlogPost, User


class BaseTestCase(TestCase):

    def create_app(self):
        current_app.config.from_object('config.TestConfig')
        return current_app

    def setUp(self):
        db.create_all()
        db.session.add(User("admin","ad@min.com", "admin",True))
        db.session.add(BlogPost("Test Post", "This is a test. Only a test","", "admin"))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()