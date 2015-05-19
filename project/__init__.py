__author__ = 'workhorse'

################################################
# import the Flask class from the flask module #
################################################

import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt



################################
# create the application object
################################
app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from project.users.views import users_blueprint
from project.home.views import home_blueprint

#register blue print
app.register_blueprint(users_blueprint)
app.register_blueprint(home_blueprint)