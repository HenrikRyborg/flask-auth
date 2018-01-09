import os
import vars
import datetime

class BaseConfig(object):
    SECRET_KEY                          = os.environ['secretKey']
    SIJAX_STATIC_PATH                   = os.path.join('.', os.path.dirname(__file__), 'app/static/js/sijax/')
    SIJAX_JSON_URI                      = 'app/static/js/sijax/json2.js'
    JSON_AS_ASCII                       = False
    TEMPLATES_AUTO_RELOAD               = True
    SQLALCHEMY_DATABASE_URI             = os.environ['db']
    SQLALCHEMY_TRACK_MODIFICATIONS      = False
    SESSION_TYPE                        = 'sqlalchemy'
    SESSION_SQLALCHEMY_TABLE            = 'sessions'
    PERMANENT_SESSION_LIFETIME          = datetime.timedelta(hours=4)

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    AUDIT_ENABLED                       = False

class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    AUDIT_ENABLED                       = False