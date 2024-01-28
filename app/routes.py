from flask import jsonify
from . import create_app

app = create_app()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "UP"}), 200
