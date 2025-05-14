import PyPDF2
from docx import Document
import spacy
from typing import Union, List
import os

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
        return ""
    return text

def extract_text_from_docx(file_path: str) -> str:
    try:
        doc = Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        print(f"Error reading DOCX: {str(e)}")
        return ""

def extract_text_from_file(file_path: str) -> str:
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        return extract_text_from_docx(file_path)
    elif file_extension == '.txt':
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading text file: {str(e)}")
            return ""
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def preprocess_text(text: str) -> str:
    text = ' '.join(text.split())
    return text.strip() 