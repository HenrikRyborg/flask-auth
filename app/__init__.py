from flask import Flask, session
import flask_sijax
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_sessionstore import Session
from flask_login import LoginManager

# Setup Flask and read config from ConfigClass defined above
app = Flask(__name__)
app.config.from_object('config.ProductionConfig')

# Flask-sqlalchemy
db = SQLAlchemy(app)

# Flask-sijax
flask_sijax.Sijax(app)

# Flask-bootstrap
Bootstrap(app)

# Flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "auth.loginView"

# flask-session
app.config['SESSION_SQLALCHEMY'] = db
Session(app)
app.session_interface.db.create_all()

## import blueprints
from .indexView import indexBP
from .auth import auth as auth_blueprint

## Register blueprints
app.register_blueprint(indexBP, url_prefix='')
app.register_blueprint(auth_blueprint, url_prefix='')