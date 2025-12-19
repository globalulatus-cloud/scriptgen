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

Your highest priority is to generate a BALANCED and NATURAL dialogue.
The conversation must feel spoken, human, and unscripted.
One speaker must never dominate the conversation.

========================
CORE SCRIPT REQUIREMENTS
========================

1. The script must begin with a natural opener appropriate to the context, such as greetings and the reason for the conversation.

2. The script must end with a natural wrap-up, confirmation, soft closing, or final question.
   Never end abruptly.

3. Use exactly two speakers, labeled ONLY as:
   - Speaker A
   - Speaker B

4. The tone must feel natural, conversational, and professional.
   Avoid robotic, lecture-style, or overly formal language.

5. Maintain realistic conversational flow, including:
   - Clarifications
   - Small reactions
   - Acknowledgements
   - Natural pauses and pacing

6. Adapt fully to the selected language and dialect.
   Use culturally appropriate names, expressions, politeness norms, and communication style for the given locale.

7. If technical terms, abbreviations, metrics appear, or Medicine name include natural spoken pronunciations when appropriate.
   Example: “A one see”, “bee pee”, “K P I”.

8. The script must be completely original and never reuse prior content.

9. The tone must remain professional, neutral, and safe.
   Do NOT include political content, religion, sensitive social issues, offensive language, or anything that may hurt sentiments.

10. Do NOT use em dashes.
    Use normal punctuation only.

========================
NATURAL TURN BALANCE RULES (MANDATORY)
========================

1. Speakers must strictly alternate turns.
   Speaker A speaks, then Speaker B, then Speaker A, then Speaker B.

2. No speaker may take two turns in a row.

3. Each speaker may speak ONE to THREE sentences per turn.
   Two sentences is ideal.
   Three sentences are allowed only when it feels natural in spoken conversation.

4. Turn length should vary naturally.
   Short turns are acceptable, but repetitive one-line turns across many exchanges should be avoided.

5. Explanations must be broken into back-and-forth exchanges.
   Never deliver long explanations in a single turn.

6. Both speakers must actively contribute by:
   - Asking questions
   - Responding meaningfully
   - Clarifying or advancing the topic

7. If the script exceeds 10 total turns, the difference in total turns between Speaker A and Speaker B must not exceed one.

8. Occasionally allow one speaker to briefly elaborate,
   followed by a shorter response from the other speaker,
   then return to balanced pacing.

9. For Japanese, Korean, and Chinese scripts:
- Use natural spoken phrasing, not compressed written style.
- Avoid excessive ellipsis or sentence truncation.
- Allow polite expansions and confirmations typical of spoken conversation.

========================
DOMAIN-SPECIFIC RULES
========================

If the selected domain is Finance:

- Always use the correct and locally accepted currency for the selected country or region.
- Currency symbols, names, and formats must match real-world usage in that locale.
  Examples:
  - United States: USD, dollar, $
  - United Kingdom: GBP, pound, £
  - Eurozone countries: EUR, euro, €
  - Japan: JPY, yen, ¥
  - India: INR, rupee, ₹
- Do NOT mix currencies unless explicitly required by the context.
- Monetary amounts should sound natural when spoken aloud.

========================
LENGTH AND DURATION (STRICT)
========================

Length must be appropriate for the selected language.

- For English and European languages:
  Target length: {word_target} (words)

- For Japanese, Korean, Chinese, and Cantonese:
  Target length:
  - 21 minutes: approximately 3,500 to 4,500 characters
  - 41 minutes: approximately 7,000 to 9,000 characters

You MUST meet the minimum length requirement for the selected language.
Do NOT produce a short script.

If the script is too short, continue the conversation naturally until the required length is reached.
Do NOT use filler, summaries, or monologues to increase length.
Expand only through realistic dialogue.

========================
INSERT THESE VARIABLES INTO THE SCRIPT
========================

- Topic: {topic}
- Language: {language}
- Dialect: {dialect}
- Domain: {domain}
- Speaker genders: {speakers}

========================
FINAL SELF-CHECK (MANDATORY)
========================

Before producing the final output, internally verify that:

- Speakers alternate perfectly throughout
- Turn length varies naturally without monologues
- No speaker dominates the conversation
- Both speakers contribute evenly and meaningfully
- Opening and closing feel natural and complete
- Currency usage is correct when Finance is selected
- The word count meets the required range

Only output the final conversation script.
Do not include explanations, notes, or validation text.
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






