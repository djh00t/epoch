from flask import Flask
from werkzeug.utils import secure_filename
from flask_session import Session
import os
from uuid import uuid4

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True  # Enable debug mode to automatically reload on code changes

    # Configure the image upload destination
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 10240 * 1024 * 1024  # Allow up to 1024 megabytes per upload session

    # Additional configuration can go here
    app.config['UPLOADS_DEFAULT_DEST'] = os.path.join(app.instance_path, 'uploads')
    app.config['UPLOADS_DEFAULT_URL'] = 'http://localhost:5000/uploads/'

    # Configure session to use filesystem instead of signed cookies
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = os.path.join(app.instance_path, 'session_files')
    Session(app)

    # Include our Routes
    from . import routes
    routes.init_app(app)

    return app
