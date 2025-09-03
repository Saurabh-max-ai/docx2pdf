import streamlit as st
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

st.set_page_config(page_title="DOCX to PDF Converter")
st.title("DOCX to PDF Converter")

uploaded = st.file_uploader("Choose a .docx file", type=["docx"])
if uploaded is not None:
    st.info("Converting...")
    pdf_bytes = docx_bytes_to_pdf_bytes(uploaded.read())
    st.success("Done! Click to download.")
    st.download_button(
        label="Download PDF",
        data=pdf_bytes,
        file_name=uploaded.name.replace(".docx", ".pdf"),
        mime="application/pdf",
    )

