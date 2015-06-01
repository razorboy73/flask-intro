################################################
# import the Flask class from the flask module #
################################################
from functools import wraps # pragma: no cover
from flask import Blueprint, render_template,request, flash,redirect, url_for, current_app # pragma: no cover
from flask.ext.login import login_required, current_user # pragma: no cover
from forms import MessageForm # pragma: no cover
from project import db # pragma: no cover
from project.models import BlogPost,Course # pragma: no cover
from project.decorators import check_confirmed
import os
from werkzeug import secure_filename
from boto.s3.connection import S3Connection
import stripe
import uuid
import sys


##########################
#### Config ##############
##########################

home_blueprint = Blueprint('home', __name__,
                            template_folder='templates') # pragma: no cover





stripe_keys = {
    'secret_key': 'sk_test_66JgwFeJaEa0NNrxgBjv9Scr',
    'publishable_key': 'pk_test_dzYx1fZrr100wb02ctTHbYUz'
}

stripe.api_key = stripe_keys['secret_key']

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

def allowed_file(filename):
    return '.' in filename and filename.lower().rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

# use decorators to link the function to a url

@home_blueprint.context_processor
def utility_processor():
    def format_price(amount):
        return u'{0:.0f}'.format(100*int(amount))
    return dict(format_price=format_price)

@home_blueprint.context_processor
def utility_processor():
    def format_price(amount):
        return u'{0:.0f}'.format(100*int(amount))
    return dict(format_price=format_price)

@home_blueprint.context_processor
def utility_processor():
    def format_price_dollars(amount):
        return u'${0:.2f}'.format(int(amount))
    return dict(format_price_dollars=format_price_dollars)

@home_blueprint.route('/', methods = ["GET", "POST"])
@home_blueprint.route('/index', methods = ["GET", "POST"])
def home():
    # return "Hello, World!"  # return a string
    #posts = BlogPost.query.filter(BlogPost.user_id==current_user.id).all()
    #posts = db.session.query(BlogPost).all()

    courses = Course.query.all()
    return render_template('base.html', courses=courses )  # render a templates , form=form, posts=posts

@home_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a templates



