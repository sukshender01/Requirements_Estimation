# input_handler.py
import streamlit as st
import io
import docx
import PyPDF2

def read_docx(file) -> str:
    try:
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception:
        return ""

def read_pdf(file) -> str:
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
        return text
    except Exception:
        return ""

def get_requirements_text():
    st.sidebar.header("Input")
    mode = st.sidebar.radio("Input type:", ["Paste text", "Upload file"])
    text = ""
    if mode == "Paste text":
        text = st.sidebar.text_area("Paste requirements here", height=200, key="paste_req")
    else:
        uploaded = st.sidebar.file_uploader("Upload file (.txt, .docx, .pdf)", type=['txt','docx','pdf'], key="upload_req")
        if uploaded:
            name = uploaded.name.lower()
            if name.endswith(".txt"):
                text = uploaded.read().decode("utf-8", errors="ignore")
            elif name.endswith(".docx"):
                text = read_docx(uploaded)
            elif name.endswith(".pdf"):
                text = read_pdf(uploaded)
    return text or ""
