from flask import Flask
from .extensions import images
from flask_uploads import configure_uploads

def create_app():
    app = Flask(__name__)
    app.config['UPLOADED_IMAGES_DEST'] = 'uploads/images'  # configure the image upload destination

    # Initialize Flask-Uploads
    configure_uploads(app, images)

    # Additional configuration can go here

    with app.app_context():
        # Include our Routes
        from . import routes

    return app
