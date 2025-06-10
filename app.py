from flask import Flask, request, jsonify
import requests
import fitz  # PyMuPDF
import tempfile
import os

API_KEY = os.environ.get("API_KEY")  # You’ll set this on Render

@app.route('/extract-text', methods=['POST'])
def extract_text():
    # 🔐 Check API key from headers
    provided_key = request.headers.get("X-API-Key")
    if provided_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    file_url = data.get("file_url")

    if not file_url:
        return jsonify({"error": "Missing file_url"}), 400

    try:
        response = requests.get(file_url)
        response.raise_for_status()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(response.content)
            temp_file_path = temp_file.name

        doc = fitz.open(temp_file_path)
        full_text = "\n\n".join([page.get_text() for page in doc])
        doc.close()

        return jsonify({"text": full_text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
