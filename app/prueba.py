from services.pdf_reader import extract_text_pdf

libro = extract_text_pdf("CV_Alejandro_Lillo.pdf")
print(libro)