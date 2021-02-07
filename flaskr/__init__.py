import os
from flask import Flask
from flask_login import LoginManager


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app


app = create_app()

# config auth
login_manager = LoginManager()
# removed strong protection below as this requires a users IP to remain constant,
# which is not appropriate when a client is behind a group of load balanced proxies
login_manager.session_protection = None  # "strong"
login_manager.init_app(app)
login_manager.login_view = "login"  # route client to login() view if they access a page requiring authentication
