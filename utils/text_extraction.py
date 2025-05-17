import pdfplumber
from docx import Document
import os

def extract_text_from_pdf(file) -> str:
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file) -> str:
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_file(file) -> str:
    # file can be a Streamlit UploadedFile or a path string
    if hasattr(file, 'name'):
        ext = os.path.splitext(file.name)[1].lower()
    else:
        ext = os.path.splitext(file)[1].lower()

    if ext == '.pdf':
        return extract_text_from_pdf(file)
    elif ext == '.docx':
        return extract_text_from_docx(file)
    elif ext == '.txt':
        try:
            if hasattr(file, 'read'):
                return file.read().decode('utf-8')
            else:
                with open(file, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            print(f"Error reading text file: {e}")
            return ""
    else:
        raise ValueError(f"Unsupported file format: {ext}")
