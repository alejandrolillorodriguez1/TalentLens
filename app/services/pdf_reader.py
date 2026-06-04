from pypdf import PdfReader
import re
def clean_pdf_text(text):
    text = re.sub(r'(?<=\b\w) (?=\w\b)', '', text)

    text = re.sub(r'\n+', '\n', text)

    text = re.sub(r' +', ' ', text)

    return text.strip()
def extract_text_pdf(path):
    reader = PdfReader(path)
    text = ""
    for pages in reader.pages : 
        text += pages.extract_text() + "\n"
    return clean_pdf_text(text)