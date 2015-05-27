__author__ = 'workhorse'
from base import BaseTestCase
import unittest
from flask import current_app


class TestTestingConfig(BaseTestCase):
    def create_app(self):
        current_app.config.from_object('config.TestConfig')
        return current_app

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
        self.assertTrue(current_app.config['DEBUG'] is True)
        self.assertTrue(current_app.config['BCRYPT_LOG_ROUNDS'] == 1)
        self.assertTrue(current_app.config['WTF_CSRF_ENABLED'] is False)

    def test_app_exists(self):
        self.assertFalse(current_app is None)


if __name__ == "__main__":
    unittest.main()