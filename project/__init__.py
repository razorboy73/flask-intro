__author__ = 'workhorse'

################################################
# import the Flask class from the flask module #
################################################

import os

from flask import Flask,render_template
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager



################################
# create the application object
################################
app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)

from project.users.views import users_blueprint
from project.home.views import home_blueprint

#register blue print
app.register_blueprint(users_blueprint)
app.register_blueprint(home_blueprint)

########################
# login view definition#
########################

from models import User
login_manager.login_view = "users.login"
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id==int(user_id)).first()


########################
#### File Uploading ####
########################
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

########################
#### error handlers ####
########################

@app.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/403.html"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500