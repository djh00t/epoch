from flask import Flask
import logging
from werkzeug.utils import secure_filename
from flask.sessions import SecureCookieSessionInterface
from flask.sessions import SessionInterface, SessionMixin
from cachelib.file import FileSystemCache
from werkzeug.datastructures import CallbackDict
import os
from uuid import uuid4

logging.basicConfig(level=logging.DEBUG)

class Session(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None):
        CallbackDict.__init__(self, initial)
        self.sid = sid
        self.modified = False

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
            session_data = self.cache.get(sid)
            if session_data is None:
                session_data = Session(initial={}, sid=sid)
                session_data = Session(initial={}, sid=sid)
                self.cache.set(sid, session_data)
            return session_data
        stored_data = self.cache.get(sid)
        if stored_data:
            return Session(initial=stored_data, sid=sid)
        return Session(initial={}, sid=sid)

    def save_session(self, app, session, response):
        sid = session.sid
        sid = session.sid
        if not session:
            if sid:
                self.cache.delete(sid)
                response.delete_cookie(app.session_cookie_name)
            return
        session.permanent = session.get('permanent', False)
        cookie_exp = self.get_expiration_time(app, session)
        self.cache.set(sid, dict(session), timeout=app.permanent_session_lifetime)
        response.set_cookie(app.session_cookie_name, sid, expires=cookie_exp, httponly=True, domain=self.get_cookie_domain(app))

    def _generate_sid(self):
        return str(uuid4())

def create_app():
    app = Flask(__name__)
    logging.debug('Creating Flask app instance')

    # Configure the image upload destination
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # Allow up to 1024 megabytes per upload session

    # Additional configuration can go here
    app.config['UPLOADS_DEFAULT_DEST'] = os.path.join(app.instance_path, 'uploads')
    app.config['UPLOADS_DEFAULT_URL'] = 'http://localhost:5000/upload/'

    # Configure session to use filesystem instead of signed cookies
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = os.path.join(app.instance_path, 'flask_session')
    app.config['SESSION_FILE_THRESHOLD'] = 500
    app.config['SESSION_FILE_MODE'] = 600
    app.session_interface = FileSystemSessionInterface(app)

    # Generate or retrieve the secret key for session signing and store it in the filesystem cache
    secret_key_cache = FileSystemCache(app.config['SESSION_FILE_DIR'], threshold=1, default_timeout=0)
    secret_key = secret_key_cache.get('secret_key')
    if not secret_key:
        secret_key = os.urandom(24)
        secret_key_cache.set('secret_key', secret_key)
    app.config['SECRET_KEY'] = secret_key
    logging.debug('Secret key set to: %s', app.config['SECRET_KEY'])

    # Configure session to use filesystem instead of signed cookies
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = os.path.join(app.instance_path, 'flask_session')
    app.config['SESSION_FILE_THRESHOLD'] = 500
    app.config['SESSION_FILE_MODE'] = 600
    app.session_interface = FileSystemSessionInterface(app)

    # Include our Routes
    from . import routes
    routes.init_app(app)

    logging.debug('App configuration: %s', app.config)

    return app
