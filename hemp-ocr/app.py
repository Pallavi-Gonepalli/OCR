# app.py

from flask import Flask, request, jsonify, render_template, redirect, url_for
from ocr_engine import extract_text_from_image
import os
import requests

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# === API ENDPOINT ===
@app.route('/ocr', methods=['POST'])
def ocr_api():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    extracted_text = extract_text_from_image(file_path)
    return jsonify({'text': extracted_text})


# === HTML PAGES ===
@app.route('/')
def home():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_page():
    if 'file' not in request.files or request.files['file'].filename == '':
        return "No file selected", 400

    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Call the internal OCR API
    with open(file_path, 'rb') as f:
        response = requests.post('http://localhost:5000/ocr', files={'file': f})

    if response.status_code == 200:
        text = response.json()['text']
        return render_template('result.html', text=text)
    else:
        return "OCR failed", 500


if __name__ == '__main__':
    app.run(debug=True)
