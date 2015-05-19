__author__ = 'workhorse'

from project import app,db
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

# config
app.config.from_object(os.environ["APP_SETTINGS"])

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)



if __name__ == '__main__':
    #app.run()
    manager.run()
    #manager.add_command("shell",Shell(make_context=make_shell_context()))
