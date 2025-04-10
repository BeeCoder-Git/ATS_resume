from dotenv import load_dotenv
import streamlit as st
import os
import PyPDF2 as pdf
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to extract text from PDF using PyPDF2
def extract_text_from_pdf(upload_file):
    if upload_file is not None:
        reader = pdf.PdfReader(upload_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        if not text.strip():
            raise ValueError("No readable text found in the uploaded PDF.")
        return [text]
    else:
        raise FileNotFoundError("No file uploaded.")

# Function to get Gemini response
def get_gemini_response(input_prompt, pdf_text, job_description):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([input_prompt, pdf_text[0], job_description])
    return response.text

# Streamlit app setup
st.set_page_config(page_title="ATS Resume Checker")
st.header("Resume Scanning System")

input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload Your Resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF Uploaded Successfully")

# Buttons
submit1 = st.button("Tell me About the Resume")
submit2 = st.button("How can I Improve my Skill")
submit3 = st.button("Percentage Match")

# Prompts
input_prompt1 = """
You are an experienced HR professional with deep technical knowledge across various domains including SOFTWARE DEVELOPMENT, DATA SCIENCE, FULL STACK, WEB DEVELOPMENT, BIG DATA ENGINEERING, CLOUD COMPUTING, DEVOPS, DATA ANALYTICS, MACHINE LEARNING, ARTIFICIAL INTELLIGENCE, CYBERSECURITY, and more.
Your task is to thoroughly review the candidate's resume against a provided job description from any technical field.
Evaluate whether the candidate aligns with the job role, highlight their strengths, and point out areas where they fall short.
Provide a professional summary of your findings in an HR-friendly tone.
"""

input_prompt2 = """
You are a skilled technical mentor and career advisor with expertise in all major technical fields including SOFTWARE DEVELOPMENT, DATA SCIENCE, MACHINE LEARNING, FULL STACK, FRONTEND/BACKEND, DEVOPS, BIG DATA, CLOUD, CYBERSECURITY, BLOCKCHAIN, and more.
Your task is to analyze the candidate's resume and suggest practical, role-specific improvements to help them upskill.
List out any missing skills, tools, certifications, or experiences that could make them a stronger candidate in their field.
Recommend suitable learning resources, online courses, or project ideas tailored to the job roles they are interested in.
"""

input_prompt3 = """
You are an intelligent ATS (Applicant Tracking System) scanner and technical evaluator with deep knowledge across all technology domains including DATA SCIENCE, SOFTWARE DEVELOPMENT, FULL STACK, DEVOPS, CLOUD COMPUTING, AI/ML, CYBERSECURITY, DATA ENGINEERING, and more.
Evaluate the candidate's resume against the provided job description and provide a percentage match that reflects how closely they align.
Start with a percentage score.
Then list the important **keywords/skills missing** from the resume.
End with **final thoughts** on what the candidate could do to improve their chances for this role.
Be precise, role-specific, and concise in your analysis.
"""

# Response handling
if submit1:
    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_text, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.warning("Please Upload the Resume")

elif submit2:
    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_text, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.warning("Please Upload the Resume")

elif submit3:
    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_text, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.warning("Please Upload the Resume")
