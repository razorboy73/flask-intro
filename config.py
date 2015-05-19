#default config
import os

class BaseConfig(object):
        DEBUG = False
        SECRET_KEY = 'Ww\x96]\xfe\xa0_\x05\xc6\xd7wN\x05\x00 /\x97\xc9\xe3Rjp\xb2\xa5x\xe4"\xe6r\xf7\xc7w\xc5\x14G\xc2dp~7:\x9e\xa6U\xebL\xf1\xa1\x94]\xbb\xa0\x96T\x1c.'
        SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]



class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
