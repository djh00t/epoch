from flask import Flask
from werkzeug.utils import secure_filename
from flask.sessions import FilesystemSessionInterface
import os
from uuid import uuid4

def create_app():
    app = Flask(__name__)

    # Configure the image upload destination
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # Allow up to 1024 megabytes per upload session

    # Additional configuration can go here
    app.config['UPLOADS_DEFAULT_DEST'] = os.path.join(app.instance_path, 'uploads')
    app.config['UPLOADS_DEFAULT_URL'] = 'http://localhost:5000/upload/'

    # Configure session to use filesystem instead of signed cookies
    app.secret_key = os.urandom(24)
    app.session_interface = FilesystemSessionInterface()

    # Include our Routes
    from . import routes
    routes.init_app(app)

    return app
