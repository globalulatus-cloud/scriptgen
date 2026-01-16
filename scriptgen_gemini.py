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
        "Cantonese Hong Kong",
        "Cantonese Chinese",
        "Chinese Hong Kong"
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
            return (7200, 8500)
        elif duration == "41":
            return (7000, 9000)
        elif duration == "55":
            return (11500, 13500)
        elif duration == "6":
            return (2280, 2400)
    
    else:
        if duration == "21":
            return (2100, 2500)
        elif duration == "31":
            return (5100, 5600)
        elif duration == "41":
            return (4100, 4800)
        elif duration == "55":
            return (7500, 8500)
        elif duration == "6":
            return (1200, 1320)


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
    "English Australia", "German Switzerland", "Cantonese Chinese", "Chinese Hong Kong","English Scotland","English Wales"
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
    "English Australia": ["Australia"],
    "German Switzerland": ["Switzerland"],
    "Cantonese Chinese": ["Chinese"],
    "Chinese Hong Kong": ["Hong Kong"],
    "English Scotland":["Scotland"]
    "English Wales":["Wales"]
}

language = st.selectbox("Language", language_options)
dialect = st.selectbox("Dialect", dialect_options.get(language, ["Default"]))

# --------------------------------------------------
# User inputs
# --------------------------------------------------
topic = st.text_input("Topic")

duration = st.selectbox(
    "Script Duration (minutes)",
    ["21", "31", "41", "55","6"]
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
# Script generation with iterative length checking
# --------------------------------------------------
def generate_script(topic, language, dialect, duration, speakers, domain):

    if is_asian_language(language):
        if duration == "21":
            length_target = "approximately 3,500 to 4,500 characters"
            length_anchor = "4,000 characters"
            min_target = 3500
            max_target = 4500
        elif duration == "31":
            length_target = "approximately 7,200 to 8,500 characters"
            length_anchor = "8,000 characters"
            min_target = 7200
            max_target = 8500
        elif duration == "41":
            length_target = "approximately 7,000 to 9,000 characters"
            length_anchor = "8,200 characters"
            min_target = 7000
            max_target = 9000
        elif duration == "55":
            length_target = "approximately 11,500 to 13,500 characters"
            length_anchor = "13,000 characters"
            min_target = 11500
            max_target = 13500
        elif duration == "6":
            length_target = "approximately 2,280 to 2,400 characters"
            length_anchor = "2,350 characters"
            min_target = 2280
            max_target = 2400
        unit = "characters"
    else:
        if duration == "21":
            length_target = "2100 to 2500 words"
            length_anchor = "2,300 words"
            min_target = 2100
            max_target = 2500
        elif duration == "31":
            length_target = "5100 to 5600 words"
            length_anchor = "5,300 words"
            min_target = 5100
            max_target = 5600
        elif duration == "41":
            length_target = "4100 to 4800 words"
            length_anchor = "4,500 words"
            min_target = 4100
            max_target = 4800
        elif duration == "55":
            length_target = "7500 to 8500 words"
            length_anchor = "8,000 words"
            min_target = 7500
            max_target = 8500
        elif duration == "6":
            length_target = "1200 to 1320 words"
            length_anchor = "1280 words"
            min_target = 1200
            max_target = 1320
        unit = "words"

    prompt = f"""
You are ScriptGen Studio, an AI assistant designed to generate realistic, natural, culturally accurate two-speaker conversation scripts.

⚠️ CRITICAL LENGTH REQUIREMENT ⚠️
YOU MUST generate a script of EXACTLY {length_target}.
This is NON-NEGOTIABLE. Target approximately {length_anchor}.

The conversation MUST continue naturally until you reach this length.
DO NOT stop early. DO NOT summarize prematurely.
Keep the dialogue flowing with natural back-and-forth exchanges.

CORE REQUIREMENTS:
- Use exactly two speakers: Speaker A and Speaker B
- Strict turn alternation (A, B, A, B...)
- One to three sentences per turn
- Natural pacing and realistic flow
- No em dashes (—)
- Balanced dialogue - neither speaker dominates

LANGUAGE AND LOCALE:
- Language: {language}
- Dialect: {dialect}
- Use culturally appropriate expressions and politeness levels

DOMAIN:
- {domain}

DOMAIN-SPECIFIC RULES:
{get_domain_rules(domain, dialect)}

TOPIC:
{topic}

SPEAKER GENDERS:
{speakers}

STRUCTURE:
1. Begin with a natural, contextually appropriate greeting
2. Develop the conversation naturally around the topic
3. Include realistic pauses, clarifications, and natural speech patterns
4. Continue the dialogue until you reach {length_anchor}
5. End with a natural closing only after meeting the length requirement
6. Ensure that you give consistant format.
7. Ensure that you give language and dilet specific names accurately to speaker A & Speaker B in the conversation.
8. If 21 minutes is selected, the speech should be delivered for a minimum of 21 minutes. If 41 minutes is selected, the speech should be delivered for a minimum of 41 minutes. If 6 minutes is selected, the speech should be delivered for a minimum of 6 minutes.
9. The total speech output must not exceed 50,000 characters. Please adjust spacing and content length accordingly.


FORBIDDEN:
- Do NOT use narrative descriptions like *pauses* or [smiles]
- Do NOT include stage directions
- Do NOT add meta-commentary
- Do NOT summarize at the end

Return ONLY the conversation script with Speaker A and Speaker B labels.
REMEMBER: The script MUST be {length_target}. Keep writing until you reach this target.
"""

    # Initial generation
    response = model.generate_content(prompt)
    script = response.text
    
    # Check length and extend if needed
    current_length, _ = get_length_metrics(script, language)
    attempts = 0
    max_attempts = 5
    
    while current_length < min_target and attempts < max_attempts:
        st.info(f"Script length: {current_length:,} {unit}. Extending... (Attempt {attempts + 1}/{max_attempts})")
        
        extension_prompt = f"""
Continue the following conversation naturally. The script is currently too short.

Current script length: {current_length} {unit}
Target length: {length_target}
You need to add approximately {min_target - current_length} more {unit}.

IMPORTANT:
- Continue with the next speaker's turn (maintain alternation)
- Keep the same natural tone and topic
- Do NOT summarize or rush to conclude
- Let the conversation develop naturally
- Only end when you've added enough content
- The total speech output must not exceed 50,000 characters. Please adjust spacing and content length accordingly.

Current script:
{script}

Continue the conversation:
"""
        
        extension_response = model.generate_content(extension_prompt)
        extension = extension_response.text
        
        # Merge the extension
        script = script.rstrip() + "\n\n" + extension.lstrip()
        current_length, _ = get_length_metrics(script, language)
        attempts += 1

    return script


def get_domain_rules(domain, dialect):
    rules = {
        "Finance": f"""
- Use the correct local currency for {dialect} ONLY
- Do NOT mix currencies
- Use realistic financial scenarios
- Include specific numbers where appropriate
""",
        "Healthcare": """
- Use appropriate medical terminology
- Show empathy and professionalism
- Include realistic patient concerns
- Maintain privacy awareness
""",
        "Call center": """
- Include authentic customer service language
- Show problem-solving approaches
- Use realistic customer inquiries
- Maintain professional courtesy
"""
    }
    return rules.get(domain, "")


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





