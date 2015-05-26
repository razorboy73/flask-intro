__author__ = 'workhorse'
# project/email.py
from flask import current_app
from flask.ext.mail import Message

from project import  mail

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html= template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)