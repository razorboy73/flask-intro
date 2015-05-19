################################################
# import the Flask class from the flask module #
################################################
from flask import Flask, flash, redirect, session, url_for, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps
import os


################################
# create the application object
################################
app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])
db = SQLAlchemy(app)

from models import *
from project.users.views import users_blueprint

#register blue print
app.register_blueprint(users_blueprint)


###########################
# login required decorator#
###########################
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('users.login'))
    return wrap


# use decorators to link the function to a url
@app.route('/')
@login_required
def home():
    # return "Hello, World!"  # return a string
    posts = db.session.query(BlogPost).all()
    return render_template('index.html', posts=posts)  # render a templates

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a templates







# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)