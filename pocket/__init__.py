import os
from flask import Flask, render_template, request, Response, send_from_directory
from flask_bootstrap import Bootstrap
import secrets

from .money import money
from .nav import nav


def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    secret = secrets.token_urlsafe(32)
    app.secret_key = secret

    app.register_blueprint(money)

    from pocket import db
    db.createdbIfNotExists() 

    nav.init_app(app)

    return app


