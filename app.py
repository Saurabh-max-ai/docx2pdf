import streamlit as st
from io import BytesIO
from docx import Document
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

# ---------- Conversion ----------
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

# ---------- Page config ----------
st.set_page_config(
    page_title="DOCX to PDF Converter",
    page_icon="📄".encode("ascii", "ignore").decode(),  # safe no-emoji fallback
    layout="centered",
)

# ---------- Minimal CSS ----------
st.markdown(
    """
    <style>
      .stApp {
        background: linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
      }
      .app-card {
        max-width: 720px;
        margin: 2rem auto;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        box-shadow: 0 10px 30px rgba(0,0,0,0.06);
        border-radius: 16px;
        padding: 28px 28px 22px;
      }
      .title {
        font-weight: 800;
        font-size: 28px;
        letter-spacing: 0.3px;
        margin-bottom: 6px;
      }
      .subtitle {
        color: #475569;
        margin-bottom: 18px;
      }
      .hint {
        font-size: 12px;
        color: #64748b;
        margin-top: 10px;
      }
      .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        margin-top: 18px;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- UI ----------
with st.container():
    st.markdown('<div class="app-card">', unsafe_allow_html=True)

    st.markdown('<div class="title">DOCX to PDF Converter</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Upload a .docx file and get a clean PDF. Best for text-based documents.</div>',
        unsafe_allow_html=True,
    )

    max_mb = 10  # file size limit
    uploaded = st.file_uploader("Choose a .docx file", type=["docx"])

    if uploaded is not None:
        size_mb = uploaded.size / (1024 * 1024)
        st.write(f"File: {uploaded.name}  |  Size: {size_mb:.2f} MB")

        if size_mb > max_mb:
            st.error(f"File is larger than {max_mb} MB. Please upload a smaller file.")
        else:
            with st.spinner("Converting..."):
                pdf_bytes = docx_bytes_to_pdf_bytes(uploaded.read())

            st.success("Conversion complete.")
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name=uploaded.name.rsplit(".", 1)[0] + ".pdf",
                mime="application/pdf",
            )

    st.markdown(
        '<div class="hint">Note: Complex Word layouts (images, columns, headers/footers) may render differently. '
        "This tool focuses on text fidelity.</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="footer">Made with Streamlit • DOCX to PDF</div>',
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)




