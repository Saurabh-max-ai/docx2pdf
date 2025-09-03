import streamlit as st
from io import BytesIO
from docx import Document
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

# ---------------- Conversion ----------------
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

# ---------------- Page setup ----------------
st.set_page_config(
    page_title="DOCX to PDF | Fast Converter",
    layout="centered",
)

# ---------------- Theming / CSS ----------------
st.markdown(
    """
    <style>
      :root { --brand:#2563eb; --ink:#0f172a; --muted:#64748b; }
      .stApp { 
        background: radial-gradient(80% 60% at 20% 0%, #eff6ff 0%, #f8fafc 40%, #eef2f7 100%);
      }
      .topbar {
        position: sticky; top: 0; z-index: 10;
        display:flex; align-items:center; gap:10px;
        padding: 14px 18px; margin: -2rem -1rem 0 -1rem;
        background: rgba(255,255,255,0.7); backdrop-filter: blur(6px);
        border-bottom: 1px solid #e5e7eb;
      }
      .logo { 
        width: 28px; height: 28px; border-radius:8px; 
        background: var(--brand); display:inline-block;
      }
      .brand { font-weight:800; color: var(--ink); letter-spacing:.3px; }
      .hero {
        max-width: 860px; margin: 36px auto 0 auto;
        text-align:left;
      }
      .h1 { font-size: 40px; line-height: 1.1; font-weight: 900; color: var(--ink); }
      .lead { color: var(--muted); margin-top: 8px; font-size: 16px; }
      .card {
        max-width: 860px; margin: 22px auto; padding: 26px 26px 20px 26px;
        background: rgba(255,255,255,0.9);
        border: 1px solid #e5e7eb; border-radius: 16px;
        box-shadow: 0 12px 30px rgba(2,6,23,0.06);
      }
      .hint { font-size: 12px; color: #6b7280; margin-top: 12px; }
      .footer { text-align:center; color:#94a3b8; font-size:12px; margin-top:22px; }
      /* Uploader polish */
      [data-testid="stFileUploader"] section div {
        border: 1px dashed #c7d2fe !important;
        background: #f8fafc !important;
      }
      [data-testid="stFileUploader"] label { color:#475569; font-weight:600; }
      .btn-row { display:flex; gap:10px; align-items:center; }
      .pill {
        display:inline-block; background:#eef2ff; color:#4338ca;
        padding:4px 10px; border-radius:999px; font-size:12px; font-weight:600;
        border:1px solid #c7d2fe;
      }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- Top bar ----------------
st.markdown(
    '<div class="topbar"><span class="logo"></span>'
    '<span class="brand">Docx2PDF</span></div>',
    unsafe_allow_html=True
)

# ---------------- Hero ----------------
st.markdown(
    '<div class="hero">'
    '<div class="h1">DOCX to PDF Converter</div>'
    '<div class="lead">Clean, fast conversion for text-based Word documents. '
    'No sign-up needed.</div>'
    '</div>',
    unsafe_allow_html=True
)

# ---------------- Main card ----------------
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1.2], vertical_alignment="center")
    with col1:
        st.write("Choose a .docx file")
    with col2:
        st.markdown('<span class="pill">Free tool</span>', unsafe_allow_html=True)

    max_mb = 15
    uploaded = st.file_uploader(" ", type=["docx"], label_visibility="collapsed")

    if uploaded is not None:
        size_mb = uploaded.size / (1024 * 1024)
        st.write(f"Selected: {uploaded.name}  |  Size: {size_mb:.2f} MB")
        if size_mb > max_mb:
            st.error(f"File is larger than {max_mb} MB. Please upload a smaller file.")
        else:
            with st.spinner("Converting to PDF..."):
                pdf_bytes = docx_bytes_to_pdf_bytes(uploaded.read())
            st.success("Conversion complete.")
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name=uploaded.name.rsplit(".", 1)[0] + ".pdf",
                mime="application/pdf",
            )

    st.markdown(
        '<div class="hint">Note: Complex Word layouts (images, columns, headers/footers)'
        ' can render differently. This tool focuses on text fidelity.</div>',
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">© Docx2PDF • Built with Streamlit</div>', unsafe_allow_html=True)





