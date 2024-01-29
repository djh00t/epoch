from flask import jsonify
from flask import jsonify, request, redirect, url_for, render_template
from . import create_app, secure_filename
import os

def init_app(app):
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "UP"}), 200

    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        if request.method == 'POST':
            # Get the uploaded files list
            uploaded_files = request.files.getlist("files")
            for file in uploaded_files:
                if file:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload'))
        return render_template('upload.html')
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "UP"}), 200

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the uploaded files list
        uploaded_files = request.files.getlist("files")
        for file in uploaded_files:
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('upload'))
    return render_template('upload.html')
