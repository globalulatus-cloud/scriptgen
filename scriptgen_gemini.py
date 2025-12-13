# Install required libraries
# Run these once on your system:
# pip install streamlit google-generativeai fpdf2

import streamlit as st
from fpdf import FPDF
import google.generativeai as genai

st.set_page_config(page_title="ScriptGen Studio", layout="wide")

st.title("ScriptGen Studio")
st.write("Generate natural two speaker scripts using Gemini 3 Pro.")

# API Key Input
api_key = st.text_input("Enter your Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

# UI Inputs
topic = st.text_input("Topic")

language = st.selectbox(
    "Language",
    ["English", "Hindi", "Korean", "Japanese"]
)

dialect_map = {
    "English": ["United States", "United Kingdom"],
    "Hindi": ["India"],
    "Korean": ["Seoul"],
    "Japanese": ["Tokyo"]
}

dialect = st.selectbox("Dialect", dialect_map.get(language, ["Standard"]))

duration = st.selectbox("Script Duration", ["21", "41"])

speakers = st.selectbox(
    "Speaker Combination",
    ["Male and Female", "Male and Male", "Female and Female"]
)

domain = st.selectbox(
    "Domain",
    ["Healthcare", "Call center", "Finance"]
)

generate = st.button("Generate Script")

# Generate Script Function
def generate_script(topic, language, dialect, duration, speakers, domain):
    if duration == "21":
        word_target = "2100 to 2500 words"
    else:
        word_target = "4100 to 4800 words"

    prompt = f"""
You are ScriptGen Studio. Create a natural two speaker conversation script.

Rules:
No em dashes.
Tone is realistic and natural.
Use correct language and dialect: {language} ({dialect}).
Speaker genders: {speakers}.
Domain: {domain}.
Topic: {topic}.
Length target: {word_target}.
Conversation should flow smoothly with turn taking.
Label speakers as Speaker A and Speaker B.

Return only the final script.
    """

    response = model.generate_content(prompt)
    return response.text

# PDF Export Function
def export_pdf(script_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font("Arial", "", fname="arial.ttf", uni=True)
    pdf.set_font("Arial", "", 12)

    for line in script_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    pdf_output = pdf.output(dest="S").encode("latin1", "ignore")
    return pdf_output


# Generate Script
if generate:
    if not api_key:
        st.error("Please enter your Gemini API key.")
    elif not topic:
        st.error("Please enter a topic.")
    else:
        with st.spinner("Generating script... please wait"):
            script = generate_script(topic, language, dialect, duration, speakers, domain)

        st.success("Script generated successfully.")
        st.text_area("Generated Script", script, height=500)

        # TXT Download
        st.download_button(
            label="Download as TXT",
            data=script,
            file_name="script.txt",
            mime="text/plain"
        )

        # PDF Download
        pdf_data = export_pdf(script)
        st.download_button(
            label="Download as PDF",
            data=pdf_data,
            file_name="script.pdf",
            mime="application/pdf"
        )
