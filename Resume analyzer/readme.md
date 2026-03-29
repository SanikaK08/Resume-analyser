# AI Resume Analyser

This project is a Streamlit-based web application that analyzes resumes using **Google Gemini AI (via GenerativeAI API)**. It extracts text from uploaded PDF resumes, evaluates the candidate's strengths, weaknesses, and skills, and optionally matches the profile with a provided job description. The result is also downloadable as a PDF.

---

## Features

- ✅ Upload a PDF resume
- ✅ Extract text using `pdfplumber` or OCR fallback via `pytesseract`
- ✅ Analyze the resume using **Gemini 1.5 Flash**
- ✅ Compare resume with job description
- ✅ Highlight skills, improvements, strengths, and weaknesses
- ✅ Download a formatted PDF of the analysis

---

## Tech Stack

- Python 3.8+
- Streamlit
- Google Generative AI SDK
- pdfplumber
- pdf2image
- pytesseract
- fpdf

---

## Installation

1. **Create a virtual environment and install dependencies**
pip install -r requirements.txt

2. **Set up Google API Key in .env**
GOOGLE_API_KEY=your_google_generative_ai_key

3. **Run the app**
streamlit run app.py



## Project Structure

resume-analyser/
│
├── app.py                  # Main Streamlit app
├── .env                    # API key file (not committed)
├── requirements.txt        # Python dependencies
└── README.md               # You're here!



## How It Works

- Uses pdfplumber to extract text from resumes.

- Falls back to pytesseract OCR for image-based PDFs.

- Sends structured prompts to Google Gemini for analysis.

- Outputs HR-style feedback including:
    Overall profile evaluation
    Skill matches and gaps
    Improvement suggestions
    Course recommendations

- Generates a downloadable PDF report.


## Sample Use Case

1. Upload your resume (PDF)

2. Paste the job description (optional)

3. Click "Analyze Resume"

4. View AI-generated feedback

5. Download the analysis report as a PDF


## Acknowledgments
- Google Generative AI
- Streamlit
- pdfplumber
- Tesseract OCR