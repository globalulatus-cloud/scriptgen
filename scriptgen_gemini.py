# Install required libraries:
# pip install streamlit google-generativeai fpdf2

import streamlit as st
from fpdf import FPDF
import google.generativeai as genai

st.set_page_config(page_title="ScriptGen Studio", layout="wide")

st.title("ScriptGen Studio")
st.write("Generate natural two speaker scripts using Gemini 2.5 Flash.")

# API key input
api_key = st.text_input("Enter your Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")


# Language and dialect dropdowns
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
    "French Canada",
    "English Australia"
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
    "English Australia": ["Australia"]
}

language = st.selectbox("Language", language_options)
dialect = st.selectbox("Dialect", dialect_options.get(language, ["Default"]))

# Other user inputs
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


# UNIVERSAL SCRIPTGEN PROMPT INSERTED HERE
def generate_script(topic, language, dialect, duration, speakers, domain):

    # Map duration into target word count
    if duration == "21":
        word_target = "2100 to 2500 words"
    else:
        word_target = "4100 to 4800 words"

    prompt = f"""
You are ScriptGen Studio, an AI assistant designed to generate realistic, natural, culturally accurate two-speaker conversation scripts.

Follow these rules for every script:

1. Start with a natural opener appropriate to the context, such as greetings and reason for the conversation.

2. End with a natural wrap-up, a final question, or a soft closing statement. Do not end abruptly.

3. Use two clearly defined speakers labeled “Speaker A” and “Speaker B”, each fulfilling their role based on the selected domain.

4. The tone must feel natural, spontaneous, and unscripted. Avoid robotic or overly formal sentences.

5. Maintain realistic conversational flow with clarifications, small interruptions, reactions, and natural pacing.

6. Adapt to the selected language and dialect. Use culturally appropriate names, phrases, references, and communication style based on the given locale.

7. Include spoken pronunciations for any technical terms or abbreviations, such as metrics, acronyms, or medical values when appropriate.

8. Ensure the script is always unique and not reused from previous outputs.

9. Keep the tone professional, neutral, and safe. 
   Absolutely avoid controversial topics, political content, sensitive social issues, religion, offensive content, or anything that can hurt sentiments.

10. Use equal turn-taking between the speakers.

11. Write with natural flow, including emotional tone when suitable.

12. No em dashes. Use normal punctuation.

13. The script length is STRICT and must match the selected duration:

    - {word_target}

    You must meet the minimum word count for the selected time. 
    Do not produce a short script. 
    If the draft is too short, automatically continue the conversation and expand it naturally until the required length is reached.

14. Before finalizing, internally check the approximate word count and ensure it fits within the target range.

Insert the following variables into the conversation:

- Topic: {topic}
- Language: {language}
- Dialect: {dialect}
- Domain: {domain}
- Speaker genders: {speakers}

Generate a full conversation script following all rules above.
Return only the script.
"""

    response = model.generate_content(prompt)
    return response.text


# PDF export using built-in Helvetica
def export_pdf(script_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=12)

    for line in script_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    return pdf.output(dest="S").encode("latin1", "ignore")


# Generate script
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

        # TXT download
        st.download_button(
            label="Download as TXT",
            data=script,
            file_name="script.txt",
            mime="text/plain",
        )

        # PDF download
        pdf_data = export_pdf(script)
        st.download_button(
            label="Download as PDF",
            data=pdf_data,
            file_name="script.pdf",
            mime="application/pdf",
        )


