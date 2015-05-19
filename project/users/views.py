###########################
#### imports ##############
###########################

from flask import flash, redirect, render_template, request,\
    session, url_for, Blueprint
from app import app
from flask.ext.bcrypt import Bcrypt
from functools import wraps


##########################
#### Config ##############
##########################
bcrypt = Bcrypt(app)
users_blueprint = Blueprint('users', __name__,
                            template_folder='templates')

###########################
# login required decorator#
###########################
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# route for handling the login page logic
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != 'admin') \
                or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@users_blueprint.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))