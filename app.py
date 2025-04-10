from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response=model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(upload_file):
    if upload_file is not None:
        # Convert the pdf into image
        images= pdf2image.convert_from_bytes(upload_file.read())

        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit app

st.set_page_config(page_title="ATS Resume Checker")
st.header("Resume Scanning System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file= st.file_uploader("Upload Your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell me About the Resume")

submit2 = st.button("How can I Improve my Skill")

submit3 = st.button("Percentage Match")

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

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please Upload the Resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please Upload the Resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please Upload the Resume")
