# utils/ocr_handler.py
import pytesseract
import fitz  # PyMuPDF
from PIL import Image
import os

def process_uploaded_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".png", ".jpg", ".jpeg", ".bmp"]:
        return extract_text_from_image(file_path)
    else:
        return "Unsupported file type."

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text if text.strip() else "No readable text found in PDF."

def extract_text_from_image(file_path):
    try:
        image = Image.open(file_path)
        return pytesseract.image_to_string(image)
    except Exception as e:
        return f"OCR failed: {str(e)}"
