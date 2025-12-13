# Install required libraries once:
# pip install streamlit google-generativeai fpdf2

import streamlit as st
from fpdf import FPDF
import google.generativeai as genai

st.set_page_config(page_title="ScriptGen Studio", layout="wide")

st.title("ScriptGen Studio")
st.write("Generate natural two speaker scripts using Gemini 2.5 Flash.")

# API Key
api_key = st.text_input("Enter your Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

# Language and Dialect Dropdowns
language_options = [
    "Spanish",
    "German",
    "Korean",
    "Traditional Chinese",
    "Spanish USA",
    "Portuguese Brazil",
    "English US",
    "English Singapore",
    "Mandarin Chinese",
    "Japanese",
    "English New Zealand",
    "Cantonese Hong Kong",
    "Spanish Mexico",
    "Italian",
    "French France",
    "English South Africa",
    "English India",
    "Portuguese Portugal",
    "French Canada"
]

dialect_options = {
    "Spanish": ["Spain"],
    "German": ["Germany"],
    "Korean": ["Korea"],
    "Traditional Chinese": ["Taiwan"],
    "Spanish USA": ["USA"],
    "Portuguese Brazil": ["Brazil"],
    "English US": ["United States"],
    "English Singapore": ["Singapore"],
    "Mandarin Chinese": ["China"],
    "Japanese": ["Japan"],
    "English New Zealand": ["New Zealand"],
    "Cantonese Hong Kong": ["Hong Kong"],
    "Spanish Mexico": ["Mexico"],
    "Italian": ["Italy"],
    "French France": ["France"],
    "English South Africa": ["South Africa"],
    "English India": ["India"],
    "Portuguese Portugal": ["Portugal"],
    "French Canada": ["Canada"],
}

language = st.selectbox("Language", language_options)
dialect = st.selectbox("Dialect", dialect_options.get(language, ["Default"]))

# Other Inputs
topic = st.text_input("Topic")

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


# Script Generation
def generate_script(topic, language, dialect, duration, speakers, domain):
    if duration == "21":
        word_target = "2100 to 2500 words"
    else:
        word_target = "4100 to 4800 words"

    prompt = f"""
You are ScriptGen Studio. Create a natural two speaker conversation script.

Rules:
No em dashes.
Language: {language}.
Dialect: {dialect}.
Speaker genders: {speakers}.
Domain: {domain}.
Topic: {topic}.
Length target: {word_target}.
Conversation must be natural with smooth turn taking.
Label speakers as Speaker A and Speaker B.
Return only the final script.
"""

    response = model.generate_content(prompt)
    return response.text


# PDF Export (Helvetica only, works everywhere)
def export_pdf(script_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=12)

    for line in script_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    return pdf.output(dest="S").encode("latin1", "ignore")


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

        # Download as TXT
        st.download_button(
            label="Download as TXT",
            data=script,
            file_name="script.txt",
            mime="text/plain",
        )

        # Download as PDF
        pdf_data = export_pdf(script)
        st.download_button(
            label="Download as PDF",
            data=pdf_data,
            file_name="script.pdf",
            mime="application/pdf",
        )
