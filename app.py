import streamlit as st
from converter import docx_bytes_to_pdf_bytes

st.set_page_config(page_title="DOCX → PDF Converter", page_icon="📄", layout="centered")
st.title("📄 DOCX → PDF Converter")
st.write("Upload a .docx file and download the converted PDF.")

uploaded = st.file_uploader("Choose a .docx file", type=["docx"])
if uploaded:
    with st.spinner("Converting..."):
        pdf_bytes = docx_bytes_to_pdf_bytes(uploaded.read())
    st.success("Done! Click to download.")
    st.download_button(⬇️ Download PDF", data=pdf_bytes,
                       file_name=uploaded.name.replace(".docx", ".pdf"),
                       mime="application/pdf")

st.caption("Note: Ye text-focused converter hai; complex Word layouts thoda different dikh sakte hain.")
