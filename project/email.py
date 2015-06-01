__author__ = 'workhorse'
# project/email.py
from flask import current_app
from flask.ext.mail import Message
from threading import Thread
from project import  mail

def send_async_email(app, msg):
    with app:
        mail.send(msg)


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html= template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    thr = Thread(target=send_async_email,args=[current_app.app_context(), msg])
    thr.start()
    return thr
