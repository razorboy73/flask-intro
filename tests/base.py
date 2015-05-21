__author__ = 'workhorse'
from flask.ext.testing import TestCase
from project import app,db
from project.models import BlogPost, User


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(BlogPost("Test Post", "This is a test. Only a test", "admin"))
        db.session.add(User("admin","ad@min.com", "admin"))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()