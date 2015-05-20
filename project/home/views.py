################################################
# import the Flask class from the flask module #
################################################
from functools import wraps
from flask import Blueprint, render_template
from flask.ext.login import login_required
from project import db
from project.models import BlogPost


##########################
#### Config ##############
##########################

home_blueprint = Blueprint('home', __name__,
                            template_folder='templates')


###########################
# login required decorator#
###########################
#not needed if using flask-login
#def login_required(f):
#    @wraps(f)
#    def wrap(*args, **kwargs):
#       if 'logged_in' in session:
#            return f(*args, **kwargs)
#        else:
#            flash('You need to login first.')
#            return redirect(url_for('users.login'))
#    return wrap


# use decorators to link the function to a url
@home_blueprint.route('/')
@login_required
def home():
    # return "Hello, World!"  # return a string
    posts = db.session.query(BlogPost).all()
    return render_template('index.html', posts=posts)  # render a templates

@home_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a templates



