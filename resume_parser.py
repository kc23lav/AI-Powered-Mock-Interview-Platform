import PyPDF2


def extract_resume_text(pdf_file):

    pdf_reader = PyPDF2.PdfReader(pdf_file)

    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text()

    return text