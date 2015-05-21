__author__ = 'workhorse'
import unittest

from flask.ext.login import current_user, request
from base import BaseTestCase
from project import bcrypt
from project.models import User


class TestUser(BaseTestCase):
     #ensure user can register
    def test_user_can_register(self):
        with self.client:
            response = self.client.post( '/register',data = dict(
                username="leigh",email="leighstern@hotmail.com",
                password="Swingline1",confirm="Swingline1",confirmed = True
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

        # Ensure errors upon incorrect registrations
    def test_incorrect_user_registration(self):
        with self.client:
            response = self.client.post( '/register',data = dict(
                username="joshuadgerbel",email="leighsternhotmail.com",
                password="Swingline1",confirm="Swingline1"
            ),follow_redirects = True)
            self.assertIn(b'Invalid email address', response.data)
            self.assertIn(b'/register', request.url)


class UsersViewsTests(BaseTestCase):
    #ensure that loging page loads correctly
    def test_login_page_loads(self):
        response = self.client.get('/login', content_type="html/text")
        self.assertTrue(b'Please Login' in response.data)


       #ensure login works with correct credentials
    def test_correct_login(self):
        with self.client:
            response = self.client.post(
                '/login', data = dict(username="admin", password="admin"),
                follow_redirects = True)
            self.assertIn(b'You were logged in.', response.data)
            self.assertTrue(current_user.name =="admin")
            self.assertTrue(current_user.is_active())

    #ensure login prevents access with incorrect
    def test_incorrect_login(self):
        response = self.client.post(
            '/login', data = dict(username="adminddd", password="admindddd"),
            follow_redirects = True)
        self.assertIn(b'Invalid Credentials. Please try again.', response.data)

    #ensure logouts works
    def test_logout(self):
        response = self.client.post(
            '/login', data = dict(username="admin", password="admin"),
            follow_redirects = True)
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'You were logged out.', response.data)

     #ensure log out page requires login
    def test_main_page_logout_required(self):
        response = self.client.get(
            '/logout', data = dict(username="admin", password="admin"),
            follow_redirects = True)
        self.assertIn(b'Please log in to access this page.', response.data)

if __name__ == "__main__":
    unittest.main()