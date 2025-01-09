from flask import Blueprint, request, jsonify
from flask_cors import CORS
import os
import pandas as pd

main = Blueprint('main', __name__)
CORS(main)  


@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file:
        os.makedirs('datasets', exist_ok=True)  
        filepath = os.path.join('datasets', file.filename)
        file.save(filepath)
        return jsonify({"message": "File uploaded successfully", "filename": file.filename}), 200

    return jsonify({"error": "File upload failed"}), 500


@main.route('/preview/<filename>', methods=['GET'])
def preview_data(filename):
    filepath = os.path.join('datasets', filename)
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath, encoding='ISO-8859-1')  # or use 'latin1'
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(filepath)
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        data = df.head(5).to_dict(orient='records')
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/clean', methods=['POST'])
def clean_data():
    data = request.get_json()
    action = data.get('action')
    filename = data.get('filename')
    columns = data.get('columns', [])

    filepath = os.path.join('datasets', filename)
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath, encoding='ISO-8859-1')
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(filepath)
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        if action == 'remove_nulls':
            df = df.dropna(subset=columns)
        elif action == 'replace_nulls':
            df = df.fillna(0)  
        elif action == 'remove_duplicates':
            df = df.drop_duplicates(subset=columns)

        cleaned_data = df.to_dict(orient='records')
        return jsonify(cleaned_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/cancel/<filename>', methods=['DELETE'])
def cancel_upload(filename):
    filepath = os.path.join('datasets', filename)
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({"message": f"File {filename} deleted successfully"}), 200
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
