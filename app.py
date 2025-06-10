from flask import Flask, request, jsonify
import requests
import fitz  # PyMuPDF
import tempfile

app = Flask(__name__)

@app.route('/extract-text', methods=['POST'])
def extract_text():
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
