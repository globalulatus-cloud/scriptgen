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
    # Configure with higher token limit
    generation_config = genai.types.GenerationConfig(
        max_output_tokens=8192,
        temperature=1.0,
    )
    model = genai.GenerativeModel("gemini-2.5-flash", generation_config=generation_config)

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
# Script generation with aggressive extension
# --------------------------------------------------
def generate_script(topic, language, dialect, duration, speakers, domain):

    if is_asian_language(language):
        if duration == "21":
            length_target = "approximately 3,500 to 4,500 characters"
            length_anchor = "4,200 characters"
            min_target = 3500
            max_target = 4500
            optimal_target = 4200
        elif duration == "31":
            length_target = "approximately 5,200 to 6,500 characters"
            length_anchor = "6,000 characters"
            min_target = 5200
            max_target = 6500
            optimal_target = 6000
        elif duration == "41":
            length_target = "approximately 7,000 to 9,000 characters"
            length_anchor = "8,200 characters"
            min_target = 7000
            max_target = 9000
            optimal_target = 8200
        elif duration == "55":
            length_target = "approximately 9,500 to 11,500 characters"
            length_anchor = "10,800 characters"
            min_target = 9500
            max_target = 11500
            optimal_target = 10800
        unit = "characters"
    else:
        if duration == "21":
            length_target = "2100 to 2500 words"
            length_anchor = "2,400 words"
            min_target = 2100
            max_target = 2500
            optimal_target = 2400
        elif duration == "31":
            length_target = "3100 to 3600 words"
            length_anchor = "3,400 words"
            min_target = 3100
            max_target = 3600
            optimal_target = 3400
        elif duration == "41":
            length_target = "4100 to 4800 words"
            length_anchor = "4,600 words"
            min_target = 4100
            max_target = 4800
            optimal_target = 4600
        elif duration == "55":
            length_target = "5500 to 6500 words"
            length_anchor = "6,200 words"
            min_target = 5500
            max_target = 6500
            optimal_target = 6200
        unit = "words"

    # Base prompt with EXTREME emphasis on length
    prompt = f"""
🚨🚨🚨 CRITICAL REQUIREMENT 🚨🚨🚨

LENGTH IS MANDATORY: {length_target}
TARGET: {length_anchor}
MINIMUM ACCEPTABLE: {min_target} {unit}

YOU MUST WRITE A LONG, DETAILED CONVERSATION.
THIS IS NOT OPTIONAL. DO NOT STOP UNTIL YOU REACH {optimal_target} {unit}.

You are generating a {duration}-minute conversation script between two speakers.
A {duration}-minute conversation requires EXTENSIVE dialogue.

═══════════════════════════════════════════════════════

TASK: Generate a natural two-speaker conversation script

LANGUAGE: {language}
DIALECT: {dialect}
DOMAIN: {domain}
TOPIC: {topic}
SPEAKERS: {speakers}

REQUIRED FORMAT:
Speaker A: [dialogue]
Speaker B: [dialogue]
Speaker A: [dialogue]
Speaker B: [dialogue]
... continue for MANY exchanges ...

CONVERSATION REQUIREMENTS:
✓ Strict alternation between speakers
✓ Natural, realistic dialogue
✓ 1-3 sentences per turn
✓ Include small talk, clarifications, and natural digressions
✓ Explore multiple aspects of the topic
✓ Add realistic details and examples
✓ Use natural conversation fillers when appropriate

{get_domain_rules(domain, dialect)}

LENGTH STRATEGY TO REACH {optimal_target} {unit}:
1. Start with proper introductions and greetings (100-200 {unit})
2. Discuss the main topic with extensive back-and-forth (70% of content)
3. Include natural tangents and follow-up questions
4. Add concrete examples and detailed explanations
5. Discuss implications, alternatives, and related topics
6. Natural wrap-up and closing (100-200 {unit})

⚠️ DO NOT:
- Rush to conclude
- Summarize at the end
- Use stage directions or descriptions
- Stop before reaching {min_target} {unit}

WRITE A COMPREHENSIVE, DETAILED CONVERSATION OF AT LEAST {min_target} {unit}.
Start now:
"""

    # Initial generation
    response = model.generate_content(prompt)
    script = response.text.strip()
    
    # Aggressive extension loop
    current_length, _ = get_length_metrics(script, language)
    attempts = 0
    max_attempts = 6  # Increased attempts
    
    progress_placeholder = st.empty()
    
    while current_length < min_target and attempts < max_attempts:
        attempts += 1
        shortfall = min_target - current_length
        
        progress_placeholder.info(
            f"📝 Extending script... Length: {current_length:,}/{min_target:,} {unit} "
            f"(Need {shortfall:,} more) - Attempt {attempts}/{max_attempts}"
        )
        
        # More aggressive extension prompt
        extension_prompt = f"""
CONTINUE THE CONVERSATION BELOW. 

CURRENT LENGTH: {current_length} {unit}
REQUIRED LENGTH: {min_target} {unit}
YOU NEED TO ADD: {shortfall} {unit}

This is a {duration}-minute conversation - it MUST be much longer.

INSTRUCTIONS:
- Continue with the NEXT speaker's turn (maintain alternation)
- Add {min(shortfall + 500, 2000)} more {unit} of dialogue
- Introduce new but related subtopics
- Ask follow-up questions
- Share additional examples and details
- Keep the conversation flowing naturally
- DO NOT conclude yet - there's still more to discuss

Current conversation:
{script}

Continue naturally with the next speaker:
"""
        
        extension_response = model.generate_content(extension_prompt)
        extension = extension_response.text.strip()
        
        # Clean up the extension (remove any speaker labels if it repeats the last line)
        lines = script.split('\n')
        extension_lines = extension.split('\n')
        
        # Merge without duplication
        if lines[-1].strip() and extension_lines[0].strip():
            # Check if extension starts with a speaker label
            if 'Speaker A:' in extension_lines[0] or 'Speaker B:' in extension_lines[0]:
                script = script + "\n" + extension
            else:
                # Extension is continuing mid-sentence, append to last line
                script = script + " " + extension
        else:
            script = script + "\n" + extension
        
        current_length, _ = get_length_metrics(script, language)
    
    progress_placeholder.empty()
    
    # Final warning if still too short
    if current_length < min_target:
        st.warning(
            f"⚠️ Reached maximum extension attempts. "
            f"Script is {current_length:,} {unit} (target: {min_target:,}+). "
            f"Try regenerating or adjust your topic to allow for more discussion."
        )
    
    return script


def get_domain_rules(domain, dialect):
    rules = {
        "Finance": f"""
DOMAIN RULES - FINANCE:
- Currency: Use ONLY the local currency for {dialect}
- Include: account numbers, transaction amounts, dates
- Topics: savings, loans, investments, budgeting, financial planning
- Be specific with numbers and financial terms
""",
        "Healthcare": """
DOMAIN RULES - HEALTHCARE:
- Use: medical terminology, symptoms, treatments
- Include: appointment scheduling, test results, medication
- Topics: patient care, medical history, health concerns
- Show empathy and professionalism
""",
        "Call center": """
DOMAIN RULES - CALL CENTER:
- Include: account verification, issue description, troubleshooting
- Topics: billing, technical support, complaints, inquiries
- Use: professional customer service language
- Add: realistic pauses for "checking systems"
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
        with st.spinner("🎬 Generating script... This may take a minute for longer
