__author__ = 'workhorse'

from base import BaseTestCase
import unittest
from flask.ext.login import current_user


class FlaskTestCase(BaseTestCase):
    # Ensure that flask was set up correctly
    def test_index(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    #ensure main page requires login
    def test_main_route_login_required(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertTrue(b"Please log in to access this page." in response.data)

    # Ensure that welcome page loads
    def test_welcome_route_works_as_expected(self):
        response = self.client.get('/welcome', follow_redirects=True)
        self.assertIn(b'Welcome to Flask!', response.data)

    # Ensure that posts show up on the main page
    def test_posts_show_up_on_main_page(self):
        response = self.client.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'This is a test. Only a test', response.data)



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


if __name__ == '__main__':
    unittest.main()