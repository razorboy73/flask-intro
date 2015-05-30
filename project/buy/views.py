__author__ = 'workhorse'

from flask import flash, redirect, render_template, request,\
     url_for, Blueprint, current_app, abort # pragma: no cover
from flask.ext.login import login_user,login_required, logout_user, current_user # pragma: no cover
from functools import wraps #- not needed with flask login
from project.models import User, BlogPost, Purchase, Course, bcrypt  # pragma: no cover
from project import db # pragma: no cover
from project.token import generate_confirmation_token, confirm_token #pragma: no cover
from project.email import send_email
import datetime #pragma: no cover
from flask.ext.admin import BaseView, expose, Admin
from flask.ext.admin.contrib.sqla import ModelView
from functools import wraps
import stripe
import uuid
import sys




##########################
#### Config ##############
##########################

buy_blueprint = Blueprint('buy', __name__,
                            template_folder='templates') # pragma: no cover


stripe_keys = {
    'secret_key': 'sk_test_66JgwFeJaEa0NNrxgBjv9Scr',
    'publishable_key': 'pk_test_dzYx1fZrr100wb02ctTHbYUz'
}

stripe.api_key = stripe_keys['secret_key']



##############
# ADMIN ######
##############
class CourseView(ModelView):
    # Disable model creation

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.is_admin()

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('users.login', next=request.url))



    # Override displayed fields
    column_list = ("course_name", "course_description", "course_location", "start_date","end_date",
                 "start_time","end_time","max_number_students","spaces_left","is_active", "price")



    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(CourseView, self).__init__(Course, session, **kwargs)



class PurchaseView(ModelView):
    # Disable model creation

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.is_admin()

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('users.login', next=request.url))



    # Override displayed fields
    column_list = ( "email", "product_id", "product","payment_method","notes","date_purchased")

    def create_model(self, form):
        model = self.model(
        form.email.data,
        form.product.data, form.payment_method.data, form.notes.data,
        form.date_purchased.data
        )
        form.populate_obj(model)
        self.session.add(model)
        self.on_model_change(form, model, True)
        self.session.commit()
        return redirect(url_for('home.home'))

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(PurchaseView, self).__init__(Purchase, session, **kwargs)


@buy_blueprint.route('/courses', methods=["GET", "POST"])
def courses():
    courses = Course.query.all()


    return render_template("home-index.html", courses=courses, key=stripe_keys['publishable_key'])

@buy_blueprint.context_processor
def utility_processor():
    def format_price(amount):
        return u'{0:.0f}'.format(100*int(amount))
    return dict(format_price=format_price)



@buy_blueprint.route('/buy', methods=['POST'])
def buy():
    stripe_token = request.form['stripeToken']
    email = request.form['stripeEmail']
    course_id = request.form['course_id']
    course = Course.query.get(course_id)
    try:
        charge = stripe.Charge.create(
                amount=int(int(course.price) * 100),
                currency='cad',
                card=stripe_token,
                description=email)
    except stripe.CardError, e:
        return """<html><body><h1>Card Declined</h1><p>Your chard could not
        be charged. Please check the number and/or contact your credit card
        company.</p></body></html>"""
    print charge
    purchase = Purchase(uuid=str(uuid.uuid4()),
            email=email,
            product=course)
    course.spaces_left -=1
    db.session.add(purchase)
    db.session.commit()
    subject='Thanks for your purchase!'
    html=render_template("purchase.html")
    send_email(email, subject, html)
    return redirect(url_for('users.login'))


@buy_blueprint.route('/test')
def test():
    return """
<http><body><form action="buy" method="POST">
<script
    src="https://checkout.stripe.com/checkout.js" class="stripe-button"
    data-key="pk_test_w3qNBkDR8A4jkKejBmsMdH34"
    data-amount="999"
    data-name="jeffknupp.com"
    data-description="Writing Idiomatic Python 3 PDF ($9.99)">
</script>
<input type="hidden" name="product_id" value="2" />
</form>
</body>
</html>
"""

if __name__ == '__main__':
    sys.exit(current_app.run(debug=True))