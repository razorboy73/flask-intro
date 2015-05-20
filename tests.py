__author__ = 'workhorse'
from project import app,db
from project.models import BlogPost, User
from flask.ext.testing import TestCase
from flask.ext.login import current_user
import unittest



class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(BlogPost("Test Post", "This is a test. Only a test", 1))
        db.session.add(User("admin","ad@min.com", "admin"))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()




class FlaskTestCase(BaseTestCase):

    # Ensure that flask was set up correctly
    def test_index(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)



   #ensure main page requires login
    def test_main_route_login_required(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertTrue(b"Please log in to access this page." in response.data)

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

    #ensure user can register
    def test_user_can_register(self):
        with self.client:
            response = self.client.post(
                '/register',
                data = dict(username="leigh",
                            email="leighstern@hotmail.com",
                            password="Swingline1",
                            confirm="Swingline1"
                            ),
                follow_redirects = True)
            self.assertIn(b'Welcome to Flask!', response.data)
            self.assertTrue(current_user.name =="leigh")
            self.assertTrue(current_user.is_active())

if __name__ == '__main__':
    unittest.main()