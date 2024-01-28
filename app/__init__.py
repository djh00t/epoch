from flask import Flask
from .extensions import images
from flask_uploads import configure_uploads

def create_app():
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Allow up to 16 megabytes file uploads
    app.config['UPLOADED_IMAGES_DEST'] = 'uploads/images'  # configure the image upload destination

    # Initialize Flask-Uploads
    configure_uploads(app, images)

    # Additional configuration can go here
    app.config['UPLOADS_DEFAULT_DEST'] = os.path.join(app.instance_path, 'uploads')
    app.config['UPLOADS_DEFAULT_URL'] = 'http://localhost:5000/uploads/'

    with app.app_context():
        # Include our Routes
        from . import routes

    return app
