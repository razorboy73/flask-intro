###########################
#### imports ##############
###########################

from flask import flash, redirect, render_template, request,\
     url_for, Blueprint, abort # pragma: no cover
from flask.ext.login import login_user,login_required, logout_user, current_user # pragma: no cover
from functools import wraps #- not needed with flask login
from forms import LoginForm, RegisterForm, PasswordField, AdminUserCreateForm, AdminUserUpdateForm # pragma: no cover
from project.models import User, BlogPost, Course, Instructor, bcrypt  # pragma: no cover
from project import db # pragma: no cover
from project.token import generate_confirmation_token, confirm_token #pragma: no cover
from project.email import send_email
import datetime #pragma: no cover
from flask.ext.admin import BaseView, expose, Admin
from flask.ext.admin.contrib.sqla import ModelView
from functools import wraps


##########################
#### Config ##############
##########################

users_blueprint = Blueprint('users', __name__,
                            template_folder='templates') # pragma: no cover

################################
# login required decorator######
# not needed with flask login###
################################
def admin_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin():
            return abort(403)
        return func(*args, **kwargs)
    return decorated_view
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



@users_blueprint.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash("The confirmation link is invalid or has expired.", "danger")
        return redirect(url_for('users.login'))
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('home.home'))

@users_blueprint.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            email = form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()

        token = generate_confirmation_token(user.email)
        confirm_url = url_for("users.confirm_email", token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.email, subject, html)
        login_user(user) #may want to  removed - want to force user to authenticate before logging in


        return redirect(url_for("users.unconfirmed"))
    return render_template('register.html', form=form)


@users_blueprint.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('home.home')
    flash('Please confirm your account!', 'warning')
    return render_template('unconfirmed.html')



@users_blueprint.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('users.confirm_email', token=token, _external=True)
    html = render_template("activate.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash("A new confirmation email has been sent.","success")
    return redirect(url_for("users.unconfirmed"))


##################
## Admin #########
##################

class MyView(BaseView):
    @expose("/")
    def index(self):
        return self.render("index-admin.html")

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.is_admin()

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))

class MyView(ModelView):
    # Disable model creation


    # Override displayed fields
    column_list = ('name', 'email','admin','registered_on')

    def create_model(self, form):
        model = self.model(
        form.name.data, form.email.data, form.password.data,
        form.admin.data
        )
        form.populate_obj(model)
        self.session.add(model)
        self.on_model_change(form, model, True)
        self.session.commit()
        return redirect(url_for('home.home'))

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(MyView, self).__init__(User, session, **kwargs)


class PostView(ModelView):
    # Disable model creation
    can_create = False

    # Override displayed fields
    column_list = ('title', 'description')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(PostView, self).__init__(BlogPost, session, **kwargs)


class CourseView(ModelView):
    # Disable model creation
    can_create = False

    # Override displayed fields
    #column_list = ('title', 'description')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(CourseView, self).__init__(Course, session, **kwargs)


class InstructorView(ModelView):
    # Disable model creation
    can_create = False

    # Override displayed fields
    #column_list = ('title', 'description')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(InstructorView, self).__init__(Instructor, session, **kwargs)

"""
class MyAdminIndexView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_admin()

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))

class UserAdminView(ModelView):
    column_searchable_list = ('name',)
    column_sortable_list = ('name', 'admin', 'email','registered_on')
    column_exclude_list = ('password',)
    form_excluded_columns = ('password',)
    form_edit_rules = ('name', 'admin','email')

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.is_admin()

    def scaffold_form(self):
        form_class = super(UserAdminView, self).scaffold_form()
        form_class.password = PasswordField('Password')
        return form_class

    def create_model(self, form):
        model = self.model(
        form.name.data, form.email.data, form.password.data,
        form.admin.data
        )
        form.populate_obj(model)
        self.session.add(model)
        self._on_model_change(form, model, True)
        self.session.commit()

class BlogAdminView(ModelView):
    column_searchable_list = ('title','user_id')
    column_sortable_list = ('title', 'description', 'user_id')
    form_edit_rules = ('title', 'description')

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.is_admin()

    def scaffold_form(self):
        form_class = super(BlogAdminView, self).scaffold_form()
        return form_class
"""
