# utils/whisper_handler.py
from faster_whisper import WhisperModel

# Load the model once with optimized settings
model = WhisperModel("base", compute_type="int8")

def transcribe_audio(audio_path):
    segments, _ = model.transcribe(audio_path, beam_size=5, language="en")
    result = ""
    for segment in segments:
        result += segment.text.strip() + " "
    return result.strip()
