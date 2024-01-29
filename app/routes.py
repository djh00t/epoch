from flask import jsonify
from flask import jsonify, request, redirect, url_for, render_template
from . import create_app, secure_filename
import os
from flask import session

def init_app(app):
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "UP"}), 200

    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        if request.method == 'POST':
            # Ensure the session has a unique identifier
            if 'session_id' not in session:
                session['session_id'] = str(uuid4())
            session_id = session['session_id']

            # Get the uploaded files list
            uploaded_files = request.files.getlist("files")
            for file in uploaded_files:
                if file:
                    filename = secure_filename(file.filename)
                    # Create a session-specific subdirectory in the upload path
                    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
                    os.makedirs(upload_path, exist_ok=True)
                    file.save(os.path.join(upload_path, filename))
            return redirect(url_for('upload'))
        return render_template('upload.html')

