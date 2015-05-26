__author__ = 'workhorse'

################################################
# import the Flask class from the flask module #
################################################

import os
import sys
import logging
from flask import Flask,render_template, Blueprint
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
#from flask.ext.admin import Admin
#from flask.ext.admin.contrib.sqla import ModelView



################################
# create the application object
################################

db = SQLAlchemy()
mail = Mail()
bcrypt = Bcrypt()
login_manager = LoginManager()
#admin = Admin()



def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    db.init_app(app)
    #admin.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)


    from project.users.views import users_blueprint
    from project.home.views import home_blueprint


    #register blue print
    app.register_blueprint(users_blueprint)
    app.register_blueprint(home_blueprint)

    # Other admin configuration as shown in last recipe

    import project.users.views as views
    #admin.add_view(views.HelloView(name='Hello'))
    #admin.add_view(ModelView(views.User, db.session))
    #admin.add_view(ModelView(views.BlogPost, db.session))
    #admin.add_view(views.UserAdminView(views.User, db.session))

    return app




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

