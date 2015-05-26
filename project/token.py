# project/token.py
###########
##imports##
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email,salt=current_app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, experation=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=experation
        )
    except:
        return False
    return email


