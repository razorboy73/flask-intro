__author__ = 'workhorse'
import unittest

from flask.ext.login import current_user
from base import BaseTestCase
from project import bcrypt
from project.models import User


class TestUser(BaseTestCase):
     #ensure user can register
    def test_user_can_register(self):
        with self.client:
            response = self.client.post( '/register',data = dict(
                username="leigh",email="leighstern@hotmail.com",
                password="Swingline1",confirm="Swingline1"
            ),follow_redirects = True)
            self.assertIn(b'Welcome to Flask!', response.data)
            self.assertTrue(current_user.name =="leigh")
            self.assertTrue(current_user.is_active())
            user = User.query.filter_by(email="leighstern@hotmail.com").first()
            self.assertTrue(str(user) == "<name - leigh>")

    def test_get_by_id(self):
        #ensure id is correct for logged in user
        with self.client:
            self.client.post('/login', data= dict(
                username = "admin",
                password = "admin"),
                follow_redirects = True)
            self.assertTrue(current_user.id == 1)
            self.assertFalse(current_user.id ==20)

    def test_check_password(self):
        #ensure passowrd is correct after unhassing
        user = User.query.filter_by(email='ad@min.com').first()
        self.assertTrue(bcrypt.check_password_hash(user.password, 'admin'))
        self.assertFalse(bcrypt.check_password_hash(user.password, 'foobar'))

if __name__ == "__main__":
    unittest.main()