# utils/gpt_handler.py
import os
from openai import OpenAI

# No 'proxies' used here
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def generate_gpt_response(prompt):
    try:
        chat_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a multilingual medical assistant named VitalAssist."},
                {"role": "user", "content": prompt}
            ]
        )
        return chat_response.choices[0].message.content.strip()
    except Exception as e:
        return f"[GPT ERROR]: {e}"
