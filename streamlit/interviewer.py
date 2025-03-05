import streamlit as st
import os
from dotenv import load_dotenv
import openai
from reportlab.pdfgen import canvas

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"

def generate_questions(role, num, skills, experience, projects):
    prompt = f"Generate {num} personalized interview questions for a candidate applying for the role of {role}. The questions should be a mix of technical, behavioral, and HR questions. Focus on evaluating the candidate's skills: {skills}, work experience: {experience}, and projects: {projects}. Include scenario-based questions, problem-solving questions, and questions that assess the candidate's contribution to past projects."
    response = openai.chat.completions.create(
        model=DEFAULT_OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "Generate interview questions for a job role."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.split("\n")

def generate_pdf(content, filename):
    pdf = canvas.Canvas(filename)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 800, "📄 Interview Questions")

    y = 780
    for i, line in enumerate(content.split("\n"), start=1):
        if y < 50:
            pdf.showPage()
            y = 800
        pdf.drawString(100, y, f"{i}. {line}")
        y -= 20

    pdf.save()

st.set_page_config(layout="wide", page_title="AI Interview Questions Generator", page_icon="💼")
st.title("💼 AI Interview Questions Generator")
st.markdown("Welcome to the AI Interview Questions Generator! This app will help you generate personalized interview questions for a job role. Simply fill in the required fields and click the 'Generate Questions' button to get started.")
st.sidebar.header("📌 Customize Your Questions")

role = st.sidebar.text_input("🔍 Job Role", placeholder="e.g. Data Scientist")
skills = st.sidebar.text_area("🛠️ Key Skills", placeholder="e.g. Python, Machine Learning, Data Structures", height=100)
experience = st.sidebar.text_area("💼 Work Experience", placeholder="e.g. 2 years in software development", height=100)
projects = st.sidebar.text_area("🚀 Projects", placeholder="e.g. Built a recommendation system", height=100)
num_questions = st.sidebar.slider("🔥 Number of Questions", 1, 20, 10)

if st.sidebar.button("🚀 Generate Questions"):
    if not role or not skills or not experience or not projects:
        st.warning("⚠️ Please fill in all fields before generating questions.")
    questions = generate_questions(role, num_questions, skills, experience, projects)
    st.success("✅ Questions Generated!")
    st.write("\n".join(questions))

    generate_pdf("\n".join(questions), "Interview_Questions.pdf")
    with open("Interview_Questions.pdf", "rb") as file:
        st.download_button("📄 Download Questions as PDF", file, "Interview_Questions.pdf", "application/pdf")
