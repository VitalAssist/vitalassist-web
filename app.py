# app.py
import os
from flask import Flask, render_template, request, jsonify
from utils.ocr_handler import process_uploaded_file
from utils.tts_handler import generate_tts
from utils.gpt_handler import generate_gpt_response
from utils.whisper_handler import transcribe_audio
import tempfile

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process_text():
    text = request.form.get("text")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    reply = generate_gpt_response(text)
    audio_path = generate_tts(reply)
    return jsonify({"response": reply, "audio": f"/static/{os.path.basename(audio_path)}"})

@app.route("/upload", methods=["POST"])
def process_file():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    with tempfile.NamedTemporaryFile(delete=False) as temp:
        file.save(temp.name)
        extracted_text = process_uploaded_file(temp.name)
        os.unlink(temp.name)

    reply = generate_gpt_response(extracted_text)
    audio_path = generate_tts(reply)
    return jsonify({"response": reply, "audio": f"/static/{os.path.basename(audio_path)}"})

@app.route("/transcribe", methods=["POST"])
def transcribe_and_process():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No audio uploaded"}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        file.save(temp.name)
        transcribed_text = transcribe_audio(temp.name)
        os.unlink(temp.name)

    reply = generate_gpt_response(transcribed_text)
    audio_path = generate_tts(reply)
    return jsonify({"transcript": transcribed_text, "response": reply, "audio": f"/static/{os.path.basename(audio_path)}"})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
