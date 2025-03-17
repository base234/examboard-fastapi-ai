import pymupdf  # PyMuPDF

def extract_pdf_text(file_path: str) -> str:
    doc = pymupdf.open(file_path)
    return "\n".join([page.get_text() for page in doc])
