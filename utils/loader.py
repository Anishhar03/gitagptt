import fitz  # PyMuPDF

def load_gita_text(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = []
    for page in doc:
        full_text.append(page.get_text())
    return "\n".join(full_text)
