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
    "English United Kingdom",
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
    "English United Kingdom": ["United Kingdom"] ,
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

Your highest priority is to generate a BALANCED, EVENLY SPOKEN dialogue.
One speaker must never dominate the conversation.

========================
MANDATORY SCRIPT RULES
========================

1. The script must begin with a natural opener appropriate to the context, such as greetings and the reason for the conversation.

2. The script must end with a natural wrap-up, soft closing, confirmation, or final question.
   Never end abruptly.

3. Use exactly two speakers, labeled ONLY as:
   - Speaker A
   - Speaker B

4. The tone must feel natural, spontaneous, and unscripted.
   Avoid robotic, lecture-style, or overly formal language.

5. Maintain realistic conversational flow, including clarifications, acknowledgements, small reactions, and natural pacing.

6. Adapt fully to the selected language and dialect.
   Use culturally appropriate names, expressions, politeness, and communication style.

7. If technical terms, abbreviations, or metrics appear, include natural spoken pronunciations when appropriate.
   Example: “A one see”, “bee pee”, “K P I”.

8. The script must be completely original and never reuse prior content.

9. The tone must remain professional, neutral, and safe.
   Do NOT include political content, religion, sensitive social issues, offensive language, or anything that may hurt sentiments.

10. Do NOT use em dashes.
    Use normal punctuation only.

========================
STRICT TURN BALANCE RULES
========================

1. Speakers must strictly alternate turns.
   Speaker A, then Speaker B, then Speaker A, then Speaker B.

2. No speaker may take two turns in a row.

3. Each speaker may speak a maximum of TWO sentences per turn.

4. No sentence may exceed 25 words.

5. Explanations must be broken into short back-and-forth exchanges.
   Never explain multiple ideas in a single turn.

6. Both speakers must ask questions, respond meaningfully, and advance the conversation.

7. If the script exceeds 10 turns, the difference in total turns between Speaker A and Speaker B must not exceed ONE.

========================
LENGTH AND DURATION (STRICT)
========================

- Target length: {word_target}

You MUST meet the minimum word count.
If the script is too short, continue the conversation naturally until the required length is reached.
Do NOT use filler, summaries, or monologues to increase length.

========================
INSERT THESE VARIABLES
========================

- Topic: {topic}
- Language: {language}
- Dialect: {dialect}
- Domain: {domain}
- Speaker genders: {speakers}

========================
FINAL SELF-CHECK
========================

Before producing the final output, internally verify:
- Perfect turn alternation
- No speaker exceeds two sentences per turn
- Sentence length stays under 25 words
- Both speakers contribute evenly
- Natural opening and closing are present
- Word count meets the required range

Only output the final conversation script.
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




