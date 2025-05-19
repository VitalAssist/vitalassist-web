# app.py
from flask import Flask, render_template, request, jsonify
from utils.ocr_handler import process_uploaded_file
from utils.tts_handler import generate_tts
import os
import tempfile

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    text = request.form.get("text")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    audio_path = generate_tts(text)
    return jsonify({"response": text, "audio": f"/static/{os.path.basename(audio_path)}"})

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    with tempfile.NamedTemporaryFile(delete=False) as temp:
        file.save(temp.name)
        extracted_text = process_uploaded_file(temp.name)
        os.unlink(temp.name)

    audio_path = generate_tts(extracted_text)
    return jsonify({"response": extracted_text, "audio": f"/static/{os.path.basename(audio_path)}"})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

