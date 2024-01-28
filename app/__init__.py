from flask import Flask

def create_app():
    app = Flask(__name__)
    # Additional configuration can go here

    with app.app_context():
        # Include our Routes
        from . import routes

    return app
