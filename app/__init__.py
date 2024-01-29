from flask import Flask
from werkzeug.utils import secure_filename
import os

def create_app():
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # Allow up to 32 megabytes file uploads

    app.config['UPLOAD_FOLDER'] = 'uploads/images'  # configure the image upload destination

    # Additional configuration can go here
    app.config['UPLOADS_DEFAULT_DEST'] = os.path.join(app.instance_path, 'uploads')
    app.config['UPLOADS_DEFAULT_URL'] = 'http://localhost:5000/uploads/'

    # Include our Routes
    from . import routes
    routes.init_app(app)

    return app
