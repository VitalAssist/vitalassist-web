# utils/gpt_handler.py
import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

def generate_gpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a multilingual medical assistant named VitalAssist."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[GPT ERROR]: {str(e)}"
