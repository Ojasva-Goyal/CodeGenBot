import streamlit as st
from src.config import VALID_TECHNIQUES, TECHNIQUE_DESCRIPTIONS
from src.theme import inject_custom_css
from src.prompts import generate_prompt_redrafts, generate_final_code
from src.utils import chat_history, add_message
from src.conversation import generate_followup_code

# Set page configuration and create a top header row with a dark mode toggle
st.set_page_config(page_title="CodeGenBot", layout="wide")
col_title, col_toggle = st.columns([0.8, 0.2])
with col_title:
    st.markdown("<h1 style='text-align: left;'>🚀 CodeGenBot: Next-Level AI-Powered Coding Assistant</h1>", unsafe_allow_html=True)
with col_toggle:
    dark_mode = st.checkbox("🌙 Dark Mode", value=False)
inject_custom_css(dark_mode)

# Expandable section for technique descriptions
with st.expander("About Prompting Techniques"):
    st.write("**Available techniques and their descriptions:**")
    for t in VALID_TECHNIQUES:
        st.markdown(f"**{t}**: {TECHNIQUE_DESCRIPTIONS[t]}")

# Initialize session states for the multi-step process if not already set
if "redrafts" not in st.session_state:
    st.session_state["redrafts"] = []
if "chosen_technique" not in st.session_state:
    st.session_state["chosen_technique"] = None
if "chosen_redraft" not in st.session_state:
    st.session_state["chosen_redraft"] = None

# Step 1: Enter coding request
st.subheader("Step 1: Enter your coding request")
user_prompt = st.text_area("What do you want CodeGenBot to do?", value="", height=100)

# Step 2: Choose a prompting technique
st.subheader("Step 2: Choose a prompting technique")
chosen_technique = st.selectbox("Pick a technique:", options=["(Select)"] + VALID_TECHNIQUES)

# Button: Generate redrafts
if st.button("Generate Redrafts"):
    if not user_prompt.strip():
        st.warning("Please enter a coding request before generating redrafts.")
    elif chosen_technique == "(Select)":
        st.warning("Please select a prompting technique.")
    else:
        st.session_state["redrafts"] = generate_prompt_redrafts(user_prompt, chosen_technique)
        st.session_state["chosen_technique"] = chosen_technique
        st.session_state["chosen_redraft"] = None

# Step 3: Choose a redraft if available
if st.session_state["redrafts"]:
    st.subheader("Step 3: Choose a redraft")
    redraft_index = st.radio(
        label="Select one of the rephrasings:",
        options=range(len(st.session_state["redrafts"])),
        format_func=lambda i: f"Option {i+1}: {st.session_state['redrafts'][i]}"
    )
    chosen_redraft = st.session_state["redrafts"][redraft_index]
    st.session_state["chosen_redraft"] = chosen_redraft

    # Button: Generate final code
    if st.button("Generate Final Code"):
        result = generate_final_code(chosen_redraft, st.session_state["chosen_technique"])
        code_snippet = result["code"]
        explanation = result["explanation"]
        st.subheader("Here is your final solution:")
        st.code(code_snippet, language="python")
        st.subheader("Explanation:")
        st.write(explanation)
        add_message("user", {"code": user_prompt, "explanation": ""})
        add_message("assistant", result)

# Follow-up conversation section
st.write("---")
st.header("Follow-up Conversation")
followup_input = st.text_input("Ask a follow-up question or refine your request:")
if st.button("Send Follow-up"):
    if followup_input.strip():
        add_message("user", {"code": followup_input, "explanation": ""})
        conv_messages = chat_history()
        assistant_result = generate_followup_code(conv_messages, followup_input)
        add_message("assistant", assistant_result)
    else:
        st.warning("Please enter a follow-up question.")

# Display conversation history
for m in chat_history():
    if m["role"] == "user":
        st.markdown(f"**You:** {m['content']['code']}")
    else:
        code_part = m["content"].get("code", "")
        expl_part = m["content"].get("explanation", "")
        st.markdown("**CodeGenBot responded:**")
        st.code(code_part, language="python")
        st.markdown(f"**Explanation:** {expl_part}")
