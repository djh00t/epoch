from flask import jsonify
from flask import jsonify, request, redirect, url_for, render_template
from . import secure_filename
from PIL import Image
import json
import io
import base64
import os
from flask import session
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
    @app.route('/logout')
    def logout():
        # Clear the session to log the user out
        session.clear()
        # Redirect to the main page or login page
        return redirect(url_for('upload'))

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
            # Create a session-specific subdirectory in the upload path
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
            os.makedirs(upload_path, exist_ok=True)
            metadata_file_path = os.path.join(upload_path, 'metadata.json')
            if not os.path.exists(metadata_file_path):
                with open(metadata_file_path, 'w') as metadata_file:
                    json.dump([], metadata_file)
            with open(metadata_file_path, 'r') as metadata_file:
                file_list = json.load(metadata_file)

            # Get the uploaded files list
            uploaded_files = request.files.getlist("files")
            new_files_added = False
            existing_filenames = {file['name'] for file in file_list}
            for uploaded_file in uploaded_files:
                if uploaded_file:
                    filename = secure_filename(uploaded_file.filename)
                    if filename in existing_filenames:
                        continue  # Skip files with conflicting names

                    file_path = os.path.join(upload_path, filename)
                    uploaded_file.save(file_path)

                    # Add file metadata to the session file list
                    file_list.append({
                        'name': filename,
                        'size': os.path.getsize(file_path),
                        'exif_date': '',  # Placeholder for EXIF date
                        'status': FILE_STATUS['OK'],
                        'progress': 100,  # Placeholder for progress
                        'thumbnail': ''  # Placeholder for thumbnail
                    })
                    new_files_added = True
                    # Create a session-specific subdirectory in the upload path
                    def create_thumbnail(file_path):
                        with Image.open(file_path) as img:
                            img.thumbnail((100, 100))
                            thumb_io = io.BytesIO()
                            img.save(thumb_io, 'JPEG', quality=85)
                            thumb_io.seek(0)
                            thumbnail_filename = f"{uuid4()}.jpeg"
                            thumbnail_path = os.path.join(upload_path, thumbnail_filename)
                            with open(thumbnail_path, 'wb') as thumb_file:
                                thumb_file.write(thumb_io.read())
                        return thumbnail_filename

                    file_path = os.path.join(upload_path, filename)
                    uploaded_file.save(file_path)

                    # Generate a low-resolution thumbnail
                    thumbnail_filename = create_thumbnail(file_path)

                    # Add file metadata to the session file list
                    file_list.append({
                        'name': filename,
                        'size': os.path.getsize(file_path),
                        'exif_date': '',  # Placeholder for EXIF date
                        'status': FILE_STATUS['OK'],
                        'progress': 100,  # Placeholder for progress
                        'thumbnail': thumbnail_filename
                    })
                    new_files_added = True

            # Save the updated file list to the metadata file
            with open(metadata_file_path, 'w') as metadata_file:
                json.dump(file_list, metadata_file)

            if new_files_added:
                # Redirect to the GET method to display the updated file list
                return redirect(url_for('upload'))
            else:
                # If no new files were added, render the template with the existing file list
                session_id = session.get('session_id', str(uuid4()))
                session['session_id'] = session_id  # Ensure the session has a unique identifier
                return render_template('upload.html', file_list=file_list, session_id=session_id)
        else:
            # Retrieve the file list from the metadata file
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], session.get('session_id', ''))
            metadata_file_path = os.path.join(upload_path, 'metadata.json')
            if os.path.exists(metadata_file_path):
                with open(metadata_file_path, 'r') as metadata_file:
                    file_list = json.load(metadata_file)
            else:
                file_list = []
            session_id = session.get('session_id', str(uuid4()))
        session['session_id'] = session_id  # Ensure the session has a unique identifier
        return render_template('upload.html', file_list=file_list, session_id=session_id)
