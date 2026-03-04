from fastapi import UploadFile
from pdfminer.high_level import extract_text
import docx
import io
import os
import inspect
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import tempfile

async def _read_file_bytes(file) -> bytes:
    read_method = getattr(file, "read", None)
    if read_method is None:
        if isinstance(file, (bytes, bytearray)):
            return bytes(file)
        raise ValueError("Unsupported input type for text extraction")

    result = read_method()
    if inspect.isawaitable(result):
        return await result
    return result


async def extract_text_from_file(file, filename: str | None = None) -> str:
    """
    Extracts text from a file, supporting .txt, .docx, .pdf, and image formats (.png, .jpg, .jpeg).
    """
    content = await _read_file_bytes(file)
    resolved_filename = filename or getattr(file, "filename", None) or getattr(file, "name", "")
    filename = resolved_filename.lower()

    if filename.endswith(".docx"):
        doc = docx.Document(io.BytesIO(content))
        return " ".join([para.text for para in doc.paragraphs])
    
    elif filename.endswith(".pdf"):
        # Try standard extraction first
        text = extract_text(io.BytesIO(content))
        if len(text.strip()) < 10:  # Likely a scanned PDF
            # Use OCR for scanned PDFs
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp.write(content)
                tmp_path = tmp.name
            
            try:
                images = convert_from_path(tmp_path)
                ocr_text = ""
                for img in images:
                    ocr_text += pytesseract.image_to_string(img)
                return ocr_text
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        return text

    elif filename.endswith((".png", ".jpg", ".jpeg")):
        # Direct OCR for images
        image = Image.open(io.BytesIO(content))
        return pytesseract.image_to_string(image)

    elif filename.endswith(".txt"):
        return content.decode("utf-8")
    
    else:
        # For other file types, attempt to decode as utf-8
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            return ""
