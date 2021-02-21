class Config(object):
    DEBUG = False
    TESTING = False

class Prod(Config):
    pass

class Dev(Config):
    DEBUG = True


