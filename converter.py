from io import BytesIO
from docx import Document
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

def docx_bytes_to_pdf_bytes(docx_bytes: bytes) -> bytes:
    bio = BytesIO(docx_bytes)
    document = Document(bio)
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    for para in document.paragraphs:
        text = para.text.strip()
        if text:
            story.append(Paragraph(text, styles["Normal"]))
            story.append(Spacer(1, 10))
    doc.build(story)
    return pdf_buffer.getvalue()
