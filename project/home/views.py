################################################
# import the Flask class from the flask module #
################################################
from functools import wraps # pragma: no cover
from flask import Blueprint, render_template,request, flash,redirect, url_for # pragma: no cover
from flask.ext.login import login_required, current_user # pragma: no cover
from forms import MessageForm # pragma: no cover
from project import db # pragma: no cover
from project.models import BlogPost # pragma: no cover
from project.decorators import check_confirmed


##########################
#### Config ##############
##########################

home_blueprint = Blueprint('home', __name__,
                            template_folder='templates') # pragma: no cover


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
@home_blueprint.route('/', methods = ["GET", "POST"])
@login_required
@check_confirmed
def home():
    # return "Hello, World!"  # return a string
    error = None
    form = MessageForm(request.form)
    if form.validate_on_submit():
        new_message = BlogPost(
            form.title.data,
            form.description.data,
            current_user.id
        )
        db.session.add(new_message)
        db.session.commit()
        flash("New entry was successfully posted.  Thanks.")
        return redirect(url_for('home.home'))
    else:
        posts = db.session.query(BlogPost).all()
    return render_template('index.html', form=form, posts=posts)  # render a templates

@home_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a templates



