from flask import Flask
from werkzeug.utils import secure_filename
from flask.sessions import SecureCookieSessionInterface
from flask.sessions import SessionInterface, SessionMixin
from cachelib.file import FileSystemCache
import os
from uuid import uuid4

class FileSystemSessionInterface(SessionInterface):
    session_cookie_name = 'session'

    def __init__(self, app):
        self.cache = FileSystemCache(app.config['SESSION_FILE_DIR'],
                                     threshold=app.config['SESSION_FILE_THRESHOLD'],
                                     mode=app.config['SESSION_FILE_MODE'])

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_interface.session_cookie_name)
        if not sid:
            sid = self._generate_sid()
            return self.cache.get(sid) or self.cache.new()
        return self.cache.get(sid)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            self.cache.delete(session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name, domain=domain)
            return
        cookie_exp = self.get_expiration_time(app, session)
        val = self.cache.set(session.sid, dict(session), timeout=app.permanent_session_lifetime)
        response.set_cookie(app.session_cookie_name, session.sid,
                            expires=cookie_exp, httponly=True, domain=domain)

    def _generate_sid(self):
        return str(uuid4())

def create_app():
    app = Flask(__name__)

    # Configure the image upload destination
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # Allow up to 1024 megabytes per upload session

    # Additional configuration can go here
    app.config['UPLOADS_DEFAULT_DEST'] = os.path.join(app.instance_path, 'uploads')
    app.config['UPLOADS_DEFAULT_URL'] = 'http://localhost:5000/upload/'

    # Set the secret key for session signing
    app.config['SECRET_KEY'] = '38CF8089-7545-4D21-A169-BB1871F0A633'

    # Configure session to use filesystem instead of signed cookies
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = os.path.join(app.instance_path, 'flask_session')
    app.config['SESSION_FILE_THRESHOLD'] = 500
    app.config['SESSION_FILE_MODE'] = 600
    app.session_interface = FileSystemSessionInterface(app)

    # Include our Routes
    from . import routes
    routes.init_app(app)

    return app
