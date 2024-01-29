from flask import jsonify
from flask import jsonify, request, redirect, url_for, render_template
from . import create_app, secure_filename
from PIL import Image
import io
import base64
import os
from uuid import uuid4
from flask import session

FILE_STATUS = {
    'READY_TO_UPLOAD': 'Ready to Upload',
    'UPLOADING': 'Uploading',
    'EXTRACTING_EXIF': 'Extracting EXIF',
    'IDENTIFYING_SUBJECT': 'Identifying Subject',
    'OK': 'OK',
    'FAILED': 'Failed'
}

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

            # Initialize or retrieve the file list for the session
            if 'file_list' not in session:
                session['file_list'] = []
            file_list = session['file_list']

            # Get the uploaded files list
            uploaded_files = request.files.getlist("files")
            for file in uploaded_files:
                if file:
                    filename = secure_filename(file.filename)
                    # Create a session-specific subdirectory in the upload path
                    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
                    os.makedirs(upload_path, exist_ok=True)
                    file_path = os.path.join(upload_path, filename)
                    file.save(file_path)

                    # Generate a low-resolution thumbnail
                    thumbnail = create_thumbnail(file_path)

                    # Add file metadata to the session file list
                    file_list.append({
                        'name': filename,
                        'size': os.path.getsize(file_path),
                        'exif_date': '',  # Placeholder for EXIF date
                        'status': FILE_STATUS['OK'],
                        'progress': 100,  # Placeholder for progress
                        'thumbnail': thumbnail
                    })

            return redirect(url_for('upload'))
        else:
            file_list = session.get('file_list', [])
            return render_template('upload.html', file_list=file_list)

    def create_thumbnail(file_path):
        with Image.open(file_path) as img:
            img.thumbnail((100, 100))
            thumb_io = io.BytesIO()
            img.save(thumb_io, 'JPEG', quality=85)
            thumb_io.seek(0)
            thumbnail = base64.b64encode(thumb_io.read()).decode('utf-8')
        return thumbnail
                    file.save(os.path.join(upload_path, filename))
            return redirect(url_for('upload'))
        return render_template('upload.html')

