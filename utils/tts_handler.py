# utils/tts_handler.py
import edge_tts
import asyncio
import uuid
import os

async def _save_tts(text, output_path):
    communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
    await communicate.save(output_path)

def generate_tts(text):
    filename = f"{uuid.uuid4()}.mp3"
    output_path = os.path.join("static", filename)
    asyncio.run(_save_tts(text, output_path))
    return output_path
