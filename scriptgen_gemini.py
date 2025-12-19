# Install required libraries:
# pip install streamlit google-generativeai fpdf2

import streamlit as st
from fpdf import FPDF
import google.generativeai as genai

# --------------------------------------------------
# Page setup
# --------------------------------------------------
st.set_page_config(page_title="ScriptGen Studio", layout="wide")

st.title("ScriptGen Studio")
st.write("Generate natural two speaker scripts using Gemini 2.5 Flash.")

# --------------------------------------------------
# Helper functions
# --------------------------------------------------
def is_asian_language(language):
    return language in [
        "Japanese",
        "Korean",
        "Traditional Chinese",
        "Mandarin Chinese",
        "Cantonese Hong Kong"
    ]


def get_length_metrics(script_text, language):
    clean_text = script_text.replace("\n", "").strip()
    if is_asian_language(language):
        return len(clean_text), "characters"
    else:
        return len(script_text.split()), "words"


def get_target_range(language, duration):
    if is_asian_language(language):
        if duration == "21":
            return (3500, 4500)
        elif duration == "31":
            return (5200, 6500)
        elif duration == "41":
            return (7000, 9000)
        elif duration == "55":
            return (9500, 11500)
    else:
        if duration == "21":
            return (2100, 2500)
        elif duration == "31":
            return (3100, 3600)
        elif duration == "41":
            return (4100, 4800)
        elif duration == "55":
            return (5500, 6500)


# --------------------------------------------------
# API key input
# --------------------------------------------------
model = None
api_key = st.text_input("Enter your Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

# --------------------------------------------------
# Language and dialect selection
# --------------------------------------------------
language_options = [
    "Spanish", "German", "Korean", "Traditional Chinese", "Spanish USA",
    "Portuguese Brazil", "English US", "English Singapore",
    "Mandarin Chinese", "Japanese", "English New Zealand",
    "Cantonese Hong Kong", "Spanish Mexico", "Italian",
    "French France", "English South Africa", "English India",
    "Portuguese Portugal", "French Canada", "English United Kingdom",
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
    "English United Kingdom": ["United Kingdom"],
    "English Australia": ["Australia"]
}

language = st.selectbox("Language", language_options)
dialect = st.selectbox("Dialect", dialect_options.get(language, ["Default"]))

# --------------------------------------------------
# User inputs
# --------------------------------------------------
topic = st.text_input("Topic")

duration = st.selectbox(
    "Script Duration (minutes)",
    ["21", "31", "41", "55"]
)

speakers = st.selectbox(
    "Speaker Combination",
    ["Male and Female", "Male and Male", "Female and Female"]
)

domain = st.selectbox(
    "Domain",
    ["Healthcare", "Call center", "Finance"]
)

generate = st.button("Generate Script")

# --------------------------------------------------
# Script generation
# --------------------------------------------------
def generate_script(topic, language, dialect, duration, speakers, domain):

    if is_asian_language(language):
        if duration == "21":
            length_target = "approximately 3,500 to 4,500 characters"
            length_anchor = "around 4,000 characters"
        elif duration == "31":
            length_target = "approximately 5,200 to 6,500 characters"
            length_anchor = "around 6,000 characters"
        elif duration == "41":
            length_target = "approximately 7,000 to 9,000 characters"
            length_anchor = "around 8,200 characters"
        elif duration == "55":
            length_target = "approximately 9,500 to 11,500 characters"
            length_anchor = "around 10,500 characters"
    else:
        if duration == "21":
            length_target = "2100 to 2500 words"
            length_anchor = "around 2,300 words"
        elif duration == "31":
            length_target = "3100 to 3600 words"
            length_anchor = "around 3,300 words"
        elif duration == "41":
            length_target = "4100 to 4800 words"
            length_anchor = "around 4,500 words"
        elif duration == "55":
            length_target = "5500 to 6500 words"
            length_anchor = "around 6,000 words"

    prompt = f"""
You are ScriptGen Studio, an AI assistant designed to generate realistic, natural, culturally accurate two-speaker conversation scripts.

Your highest priority is to generate a BALANCED and NATURAL dialogue.
The conversation must feel spoken, human, and unscripted.
One speaker must never dominate the conversation.

CORE REQUIREMENTS:
- Use exactly two speakers: Speaker A and Speaker B
- Strict turn alternation
- One to three sentences per turn
- Natural pacing and realistic flow
- No em dashes

LANGUAGE AND LOCALE:
- Language: {language}
- Dialect: {dialect}
- Use culturally appropriate expressions and politeness

DOMAIN:
- {domain}

If Finance is selected:
- Use the correct local currency only
- Do not mix currencies

LENGTH REQUIREMENT:
Target length: {length_target}
Aim for a total length of {length_anchor}

If the script is too short, continue naturally until the required length is reached.
Do not pad with summaries or monologues.

TOPIC:
{topic}

SPEAKER GENDERS:
{speakers}

Begin with a natural opener.
End with a natural closing.
Return only the conversation script.
"""

    response = model.generate_content(prompt)
    return response.text


# --------------------------------------------------
# PDF export
# --------------------------------------------------
def export_pdf(script_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=12)

    for line in script_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    return pdf.output(dest="S").encode("latin1", "ignore")


# --------------------------------------------------
# Generate and display script
# --------------------------------------------------
if generate:
    if not api_key:
        st.error("Please enter your Gemini API key.")
    elif model is None:
        st.error("Model not initialized.")
    elif not topic:
        st.error("Please enter a topic.")
    else:
        with st.spinner("Generating script... please wait"):
            script = generate_script(
                topic,
                language,
                dialect,
                duration,
                speakers,
                domain
            )

        st.success("Script generated successfully.")

        st.text_area("Generated Script", script, height=500)

        # --------------------
        # Live length feedback
        # --------------------
        count, unit = get_length_metrics(script, language)
        min_len, max_len = get_target_range(language, duration)

        st.markdown("### 📏 Script Length Check")
        st.write(f"**Detected length:** {count:,} {unit}")
        st.write(f"**Target range:** {min_len:,} to {max_len:,} {unit}")

        if count < min_len:
            st.error("❌ Script is too short for the selected duration.")
        elif count > max_len:
            st.warning("⚠️ Script exceeds the recommended length.")
        else:
            st.success("✅ Script length is within the target range.")

        st.progress(min(count / max_len, 1.0))

        # --------------------
        # Downloads
        # --------------------
        st.download_button(
            label="Download as TXT",
            data=script,
            file_name="script.txt",
            mime="text/plain",
        )

        pdf_data = export_pdf(script)
        st.download_button(
            label="Download as PDF",
            data=pdf_data,
            file_name="script.pdf",
            mime="application/pdf",
        )
