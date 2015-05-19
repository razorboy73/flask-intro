__author__ = 'workhorse'
from project import app
import unittest


class FlaskTestCase(unittest.TestCase):

    # Ensure that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)


    #ensure that loging page loads correctly
    def test_login_page_loads(self):
        tester=app.test_client(self)
        response = tester.get('/login', content_type="html/text")
        self.assertTrue(b'Please Login' in response.data)

    #ensure login works with correct credentials
    def test_correct_login(self):
        tester=app.test_client(self)
        response = tester.post(
            '/login', data = dict(username="admin", password="admin"),
            follow_redirects = True)
        self.assertIn(b'You were logged in.', response.data)


    #ensure login prevents access with incorrect
    def test_incorrect_login(self):
        tester=app.test_client(self)
        response = tester.post(
            '/login', data = dict(username="adminddd", password="admindddd"),
            follow_redirects = True)
        self.assertIn(b'Invalid Credentials. Please try again.', response.data)

    #ensure logouts works
    def test_logout(self):
        tester=app.test_client(self)
        response = tester.post(
            '/login', data = dict(username="admin", password="admin"),
            follow_redirects = True)
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'You were logged out.', response.data)

   #ensure main page requires login
    def test_main_page_login_required(self):
        tester=app.test_client(self)
        response = tester.get('/', follow_redirects=True)
        self.assertTrue(b"You need to login first." in response.data)

    #ensure posts on main page
    def test_posts_on_main_page(self):
        tester=app.test_client(self)
        response = tester.post(
            '/login', data = dict(username="admin", password="admin"),
            follow_redirects = True)
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'You were logged out.', response.data)

    #ensure log out page requires login
    def test_main_page_login_required(self):
        tester=app.test_client(self)
        response = tester.post(
            '/login', data = dict(username="admin", password="admin"),
            follow_redirects = True)
        self.assertIn(b'Title', response.data)

if __name__ == '__main__':
    unittest.main()