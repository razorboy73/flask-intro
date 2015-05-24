#default config
import os

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'Ww\x96]\xfe\xa0_\x05\xc6\xd7wN\x05\x00 /\x97\xc9\xe3Rjp\xb2\xa5x\xe4"\xe6r\xf7\xc7w\xc5\x14G\xc2dp~7:\x9e\xa6U\xebL\xf1\xa1\x94]\xbb\xa0\x96T\x1c.'
    SECURITY_PASSWORD_SALT = 'my_precious_two'
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    UPLOAD_FOLDER = os.path.realpath('.') +'/project/static/uploads'



    # gmail authentication
    MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']

    # mail accounts
    MAIL_DEFAULT_SENDER = 'from@example.com'

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    #https://github.com/jarus/flask-testing/issues/21
    #prevent AssertionError: Popped wrong request context.  (<RequestContext 'http://localhost/connect/signup' [POST] of run> instead of <RequestContext 'http://localhost/' [GET] of run>)
    BCRYPT_LOG_ROUNDS = 1


#export DATABASE_URL="postgresql://localhost/discover_flask_dev"
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = True



class ProductionConfig(BaseConfig):
    DEBUG = False
    DEBUG_TB_ENABLED = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY")