from pypdf import PdfReader

def extract_text_pdf(path):
    reader = PdfReader(path)
    text = ""
    for pages in reader.pages : 
        text += pages.extract_text() + "/n"
    return text