__author__ = 'workhorse'
# tests/test_functional.py
from project import db

import unittest

from flask.ext.login import current_user

from base import BaseTestCase
from project.models import User
from project.token import generate_confirmation_token,confirm_token


class TestPublic(BaseTestCase):

    def test_main_route_requires_login(self):
        # Ensure main route requres logged in user.
        response = self.client.get('/', follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        self.assertIn(b'Please log in to access this page', response.data)

    def test_logout_route_requires_login(self):
        # Ensure logout route requres logged in user.
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)


class TestLoggingInOut(BaseTestCase):

    def test_correct_login(self):
        # Ensure login behaves correctly with correct credentials
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(username="admin", password="admin"),
                follow_redirects=True
            )
            self.assertIn(b'Welcome', response.data)
            self.assertTrue(current_user.email == "ad@min.com")
            self.assertTrue(current_user.is_active())
            self.assertTrue(response.status_code == 200)

    def test_logout_behaves_correctly(self):
        # Ensure logout behaves correctly, regarding the session
        with self.client:
            self.client.post(
                '/login',
                data=dict(username="admin", password="admin"),
                follow_redirects=True
            )
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'You were logged out.', response.data)
            self.assertFalse(current_user.is_active())


    def test_invalid_confirmation_token(self):
        user1 = User(username="test1", email='test@test1.com', password='test1', confirmed=False)
        user2 = User(username="test2", email='test@test2.com', password='test2', confirmed=False)
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        token = generate_confirmation_token('test@test2.com')
        confirm_token(token)
        self.assertFalse(user1.confirmed)

    def test_invalid_confirmation_token_views(self):
        user1 = User(username="test1", email='test@test1.com', password='test1', confirmed=False)
        user2 = User(username="test2", email='test@test2.com', password='test2', confirmed=False)
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        token = generate_confirmation_token('test@test2.com')
        with self.client:
            self.client.post('/login', data=dict(
                username="test1", password='test1'
            ), follow_redirects=True)
            response = self.client.get(
                '/confirm/'+str(token), follow_redirects=True)
            self.assertIn('The confirmation link is invalid or has expired.',
                                response.data)
if __name__ == '__main__':
    unittest.main()