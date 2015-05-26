__author__ = 'workhorse'

from project import create_app, db
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os
import unittest
import coverage
from project.models import User
import datetime

# config
#app.config.from_object(os.environ["APP_SETTINGS"])
app = create_app(os.environ["APP_SETTINGS"])
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
@manager.command
def test():
    """runs tests without coverage"""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def cov():
    cov = coverage.coverage(branch=True, include='project/*', omit="*/__init__.py")
    cov.start()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print "Coverage Summary"
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'coverage')
    cov.html_report(directory=covdir)
    cov.erase()

@manager.command
def create_admin():
    """Creates the admin user."""
    db.session.add(User(
        username = "joshadmin22",
        email="ad@min2.com",
        password="Swingline12",
        admin=True,
        confirmed=True,
        confirmed_on=datetime.datetime.now())
    )
    db.session.commit()



if __name__ == '__main__':
    #app.run()
    manager.run()
    #manager.add_command("shell",Shell(make_context=make_shell_context()))
