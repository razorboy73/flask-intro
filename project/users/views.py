###########################
#### imports ##############
###########################

from flask import flash, redirect, render_template, request,\
     url_for, Blueprint # pragma: no cover
from flask.ext.login import login_user,login_required, logout_user # pragma: no cover
#from functools import wraps - not needed with flask login
from forms import LoginForm, RegisterForm # pragma: no cover
from project.models import User,bcrypt # pragma: no cover
from project import db # pragma: no cover


##########################
#### Config ##############
##########################

users_blueprint = Blueprint('users', __name__,
                            template_folder='templates') # pragma: no cover

################################
# login required decorator######
# not needed with flask login###
################################

#def login_required(test):
#    @wraps(test)
#    def wrap(*args, **kwargs):
#        if 'logged_in' in session:
#            return test(*args, **kwargs)
#        else:
#            flash('You need to login first.')
#            return redirect(url_for('.login'))
#    return wrap

# route for handling the login page logic
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user =User.query.filter_by(name=request.form['username']).first()
            if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):
                #session['logged_in'] = True #Not need if using flasklogin's decorators
                login_user(user)
                flash('You were logged in.')
                return redirect(url_for('home.home'))
            else:
                error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', form=form, error=error)


@users_blueprint.route('/logout')
@login_required
def logout():
    #session.pop('logged_in', None) - only needed if managing sessions
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('home.welcome'))

@users_blueprint.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            email = form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home.home'))
    return render_template('register.html', form=form)
