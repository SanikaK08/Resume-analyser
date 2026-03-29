import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import dotenv
import os
import google.generativeai as genai
import streamlit as st
from PIL import Image

dotenv.load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model=genai.GenerativeModel("gemini-1.5-flash")

def extract_text_from_pdf(pdf_path):
    text=""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text=page.extract_text()
                if page_text:
                    text+=page_text
        if text.strip():
            return text.strip()
        
    except Exception as e:
        print("Direct text extraction failed ", e)


    print("Falling back to OCR for image based pdf")
    try:
        images=convert_from_path(pdf_path)
        for image in images:
            page_text=pytesseract.image_to_string(image)
            text+=page_text+"\n"
    
    except Exception as e:
        print("OCR failed ", e)


from fpdf import FPDF

def analyze_resume(resume_text,job_description=None):
    if not resume_text:
        return {"error":"Resume text is required for analysis"}
    
    base_prompt= f"""
        You are an experienced HR with experience in the field of any job role. 
        Your task is to review the provided resume. 
        Please share your your professional evaluation as well as a score on whether the candidate's profile aligns with the role.
        Also mention skills he already has and suggest some skills to improve his resume. 
        Also suggest some course he might take to imrove his skills.
        Hightlight the strengths and weaknesses.

        Resume:
        {resume_text}

    """
    
    if job_description:
        base_prompt+= f"""
            Additionally compare this resume to following job description.

            job description:
            {job_description}

            Highlight the strengths and weaknesses of the applicant in relation to specified job description.
        """

    response=model.generate_content(base_prompt)
    analysis=response.text.strip()

    return analysis


def generate_pdf(analysis_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in analysis_text.split("\n"):
        pdf.multi_cell(0, 10, line)
    
    
    pdf_output = pdf.output(dest='S').encode('latin1')  # PDF needs latin1 encoding
    return pdf_output


#streamlit app

st.set_page_config(page_title="Resume Analyser",layout="wide")

st.title("AI Resume Analyser")
st.write("Analyse your resume and match it with job description using Google Gemini AI")

col1,col2= st.columns(2)
with col1:
    uploaded_file=st.file_uploader("upload your resume(PDF)", type=["pdf"])
with col2:
    job_description=st.text_area("Enter job description", placeholder="Enter your job description here...")


if uploaded_file is not None:
    st.success("Resume uploaded successfully")
else:
    st.warning("Please upload a resume in pdf format")


st.markdown("<div style='padding-top:10px;'></div>",unsafe_allow_html=True)

if uploaded_file:
    with open("uploaded_resume.pdf",'wb') as f:
        f. write(uploaded_file.getbuffer())

        resume_text=extract_text_from_pdf("uploaded_resume.pdf")

        if st.button("Analyse resume"):
            with st.spinner("Analysing resume"):
                try:
                    analysis=analyze_resume(resume_text,job_description)
                    st.write(analysis)
                    
                    pdf_bytes = generate_pdf(analysis)
                    st.download_button(
                        label="📄 Download Analysis PDF",
                        data=pdf_bytes,
                        file_name="resume_analysis.pdf",
                        mime="application/pdf"
                    )

                except Exception as e:
                    st.error(f"Analysis failed {e}")




