from flask import jsonify
from . import create_app
from .extensions import images
import os

app = create_app()

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
                images.save(file, name=filename)
        return redirect(url_for('upload'))
    return render_template('upload.html')
