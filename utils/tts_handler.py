# utils/tts_handler.py
import edge_tts
import asyncio
import uuid
import os
from langdetect import detect

# Language to voice mapping
VOICE_MAP = {
    "en": "en-US-AriaNeural",
    "ar": "ar-EG-SalmaNeural",
    "fa": "fa-IR-DilaraNeural",
    "hi": "hi-IN-SwaraNeural",
    "ku": "en-US-JennyNeural",  # placeholder for Kurdish
    "default": "en-US-AriaNeural"
}

async def _save_tts(text, voice, output_path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def generate_tts(text):
    try:
        lang = detect(text)
        voice = VOICE_MAP.get(lang, VOICE_MAP["default"])
    except:
        voice = VOICE_MAP["default"]

    filename = f"{uuid.uuid4()}.mp3"
    output_path = os.path.join("static", filename)
    asyncio.run(_save_tts(text, voice, output_path))
    return output_path
