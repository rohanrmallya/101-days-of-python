import streamlit as st
import os
from dotenv import load_dotenv
import openai
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from reportlab.pdfgen import canvas

# Load Environment Variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
email_sender = os.getenv("EMAIL_SENDER")
email_password = os.getenv("EMAIL_APP_PASSWORD")

# 📌 Question Generation Function
def generate_questions(role, num):
    prompt = f"Generate {num} interview questions for {role} including technical and HR questions."
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.split("\n")

# 📧 Email Sending Function
def send_email(receiver, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_sender, email_password)
        server.sendmail(email_sender, receiver, msg.as_string())
        server.quit()
        return "✅ Email Sent Successfully!"
    except Exception as e:
        return f"❌ Email Not Sent: {str(e)}"

# PDF Generation
def generate_pdf(content, filename):
    pdf = canvas.Canvas(filename)
    pdf.drawString(100, 800, "Interview Questions")
    y = 780
    for line in content.split("\n"):
        pdf.drawString(100, y, line)
        y -= 20
    pdf.save()

# Streamlit App
st.title("💪 AI Interview Questionnaire Generator")
st.sidebar.header("📌 Settings")

role = st.sidebar.text_input("Job Role")
email = st.sidebar.text_input("Candidate Email")
num_questions = st.sidebar.slider("Number of Questions", 1, 20, 10)

if st.sidebar.button("🚀 Generate Questions"):
    questions = generate_questions(role, num_questions)
    st.success("✅ Questions Generated!")
    st.write("\n".join(questions))

    # PDF Download Button
    generate_pdf("\n".join(questions), "Interview_Questions.pdf")
    with open("Interview_Questions.pdf", "rb") as file:
        st.download_button("📄 Download PDF", file, "Interview_Questions.pdf", "application/pdf")

    # Send Email Button
    email_body = f"Dear Candidate,\n\nPlease find attached interview questions for the {role} role.\n\nBest Regards,\nTeam"
    if st.sidebar.button("📧 Send Email"):
        result = send_email(email, f"{role} Interview Invitation", email_body)
        st.success(result)
