import pdfplumber

def get_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file.

    Args:
        pdf (bytes): The PDF file as bytes.

    Returns:
        str: The extracted text from the PDF.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as plumber_pdf:
            for page in plumber_pdf.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text