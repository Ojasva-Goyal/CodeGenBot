import streamlit as st
import os
import getpass
import json
import re

# If you use langchain_google_genai:
from langchain_google_genai import ChatGoogleGenerativeAI

###############################################################################
# 1. LLM Configuration
###############################################################################
# Ensure the Google API Key is set in the environment
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

# Configure the LLM (adjust model and parameters as needed)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

###############################################################################
# 2. Technique Instructions and Descriptions
###############################################################################
technique_instructions = {
    "zero_shot": "Answer directly with minimal additional context.",
    "few_shot": "Provide 1-2 brief examples before giving your main solution.",
    "chain_of_thought": "Think aloud step-by-step before finalizing the solution.",
    "least_to_most": "Break the problem into smaller sub-problems and solve them in order.",
    "self_consistency": "Generate multiple reasoning paths internally, then pick the most consistent.",
    "reflective": "Present an initial solution, then reflect and refine your answer.",
    "backtracking": "Propose a solution, then backtrack to correct any errors or inefficiencies.",
    "verbalizer": "Explicitly verbalize the reasoning and structure the final answer clearly."
}

technique_descriptions = {
    "zero_shot": (
        "No examples are given to the model. It relies purely on its internal knowledge "
        "to provide an answer directly."
    ),
    "few_shot": (
        "We supply a few brief examples before the main query, helping the model see the format "
        "or style of the desired solution."
    ),
    "chain_of_thought": (
        "The model is encouraged to 'think aloud' step by step, revealing how it arrives "
        "at the final solution (like showing its work)."
    ),
    "least_to_most": (
        "The problem is broken into smaller sub-problems, solved one by one, building up "
        "to the final solution."
    ),
    "self_consistency": (
        "The model internally generates multiple solution paths and picks the most consistent "
        "or logical final answer."
    ),
    "reflective": (
        "The model presents an initial solution, then reflects on it to refine and improve "
        "the answer."
    ),
    "backtracking": (
        "The model proposes a solution, then 'backtracks' to correct mistakes or optimize "
        "the approach."
    ),
    "verbalizer": (
        "The model explicitly verbalizes its reasoning in a structured manner, making the "
        "thought process clearer."
    )
}

valid_techniques = list(technique_instructions.keys())

###############################################################################
# 3. Base System Prompt (Strict JSON Requirement)
###############################################################################
base_system_prompt = """
You are CodeGenBot, an expert coding assistant skilled in generating code in multiple programming languages.
Your users are developers who need code solutions, code examples, or debugging assistance.

DOs:
- Provide accurate, efficient, and well-documented code.
- Ask clarifying questions if the user's request is ambiguous.
- Include an explanation of the code along with the code snippet.
- Use language-specific best practices and appropriate formatting.

DON'Ts:
- Do not provide overly generic or vague code.
- Do not include unnecessary comments or unrelated information.
- Avoid providing code that hasn't been tested or verified.

CRITICAL INSTRUCTION:
Your entire answer MUST be valid JSON. Do not include markdown formatting, triple backticks, or any text outside of the JSON. 
The JSON must have exactly two keys: "code" and "explanation".

Correct format example:
{
  "code": "...",
  "explanation": "..."
}
No additional keys, no additional text.
"""

###############################################################################
# 4. Utility Functions for JSON Extraction
###############################################################################
def extract_json_str(text: str) -> str:
    """
    Attempt to extract a valid JSON string from the text using a regex search
    for a curly-brace-enclosed object. This helps when the model adds extra text.
    """
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return match.group(0).strip()
    return ""

def parse_strict_json(raw_text: str) -> dict:
    """
    Attempt to parse 'raw_text' as strict JSON with 'code' and 'explanation'.
    Fallback to searching for { ... }, or final fallback if parsing fails.
    """
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        # Attempt regex extraction
        maybe_json = extract_json_str(raw_text)
        if maybe_json:
            try:
                data = json.loads(maybe_json)
            except json.JSONDecodeError:
                data = {
                    "code": "No valid JSON found in the response.",
                    "explanation": raw_text
                }
        else:
            data = {
                "code": "No valid JSON found in the response.",
                "explanation": raw_text
            }
    # Ensure keys exist
    if "code" not in data:
        data["code"] = "No code returned."
    if "explanation" not in data:
        data["explanation"] = "No explanation returned."
    return data

###############################################################################
# 5. Main Prompt Steps (Redrafting + Final Code)
###############################################################################
def generate_prompt_redrafts(user_prompt: str, technique: str) -> list:
    """
    Ask the LLM to produce 2-3 rephrasings of the user's prompt, guided by the technique.
    We also remind it not to include extraneous text or code blocks in the redrafts.
    """
    rephrase_instructions = f"""
You are a prompt engineer. The user provided this coding request:
"{user_prompt}"

Technique: "{technique}"

Produce 3 alternative rephrasings that apply the technique's style. 
List them clearly as:
1) ...
2) ...
3) ...
Only provide the rephrasings, nothing else.
"""
    response = llm.invoke(rephrase_instructions)
    text = response.content if hasattr(response, "content") else str(response)

    # Attempt to parse out 3 rephrasings by splitting lines at 1), 2), 3)
    redrafts = []
    lines = text.split("\n")
    current = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("1)", "2)", "3)")):
            if current:
                redrafts.append(" ".join(current).strip())
                current = []
            stripped = stripped[2:].strip()
        current.append(stripped)
    if current:
        redrafts.append(" ".join(current).strip())

    return redrafts[:3]

def generate_final_code(chosen_prompt: str, technique: str) -> dict:
    """
    Combine the chosen rephrased prompt with technique instructions and the base system prompt.
    Return a dict with 'code' and 'explanation'.
    """
    technique_extra = technique_instructions.get(technique, "")
    updated_system_prompt = (
        base_system_prompt
        + "\n\nAdditional Technique Guidance:\n"
        + technique_extra
    )

    # Build a final prompt for code generation
    full_prompt = (
        f"{updated_system_prompt}\n\n"
        f"User Request:\n{chosen_prompt}\n\n"
        "IMPORTANT: Return valid JSON only, with keys 'code' and 'explanation'."
    )
    response = llm.invoke(full_prompt)
    raw_text = response.content if hasattr(response, "content") else str(response)

    return parse_strict_json(raw_text)

###############################################################################
# 6. Follow-up Conversation
###############################################################################
def chat_history():
    """
    Return or initialize a list of messages in st.session_state for follow-up conversation.
    Each message is a dict: {"role": "user"/"assistant", "code": "...", "explanation": "..."} 
    or possibly just text if something goes awry.
    """
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    return st.session_state["messages"]

def add_message(role: str, content: dict):
    """
    Append a new message (dict with code and explanation) to the conversation history.
    """
    messages = chat_history()
    messages.append({"role": role, "content": content})

def generate_followup_code(conversation_messages: list, user_message: str) -> dict:
    """
    Use the entire conversation context + the new user message to produce a code+explanation JSON response.
    We'll maintain the same strict JSON approach for follow-ups.
    """
    conversation_text = ""
    for m in conversation_messages:
        if m["role"] == "user":
            conversation_text += f"User said:\n{m['content']}\n\n"
        else:
            code_part = m["content"].get("code", "")
            expl_part = m["content"].get("explanation", "")
            conversation_text += f"Assistant responded with code:\n{code_part}\n\nExplanation:\n{expl_part}\n\n"

    followup_prompt = (
        f"{base_system_prompt}\n\n"
        "Here is the conversation so far:\n"
        f"{conversation_text}\n"
        f"Now the user says:\n{user_message}\n\n"
        "IMPORTANT: Return valid JSON only, with keys 'code' and 'explanation'."
    )
    response = llm.invoke(followup_prompt)
    raw_text = response.content if hasattr(response, "content") else str(response)

    return parse_strict_json(raw_text)

###############################################################################
# 7. Light/Dark Mode - Top-Right Toggle
###############################################################################
def inject_custom_css(dark_mode: bool):
    """
    Inject CSS to change background/text colors. 
    We'll also place the toggle in the top-right corner using columns.
    """
    if dark_mode:
        st.markdown(
            """
            <style>
            /* Dark mode background and text */
            body, .main, .block-container {
                background-color: #0f0f0f !important;
                color: #FFFFFF !important;
            }
            /* Input elements (text boxes, radio, etc.) */
            textarea, input, .stRadio, .stSelectbox, .stTextArea {
                background-color: #333333 !important;
                color: #FFFFFF !important;
            }
            /* Titles and text */
            h1, h2, h3, h4, h5, h6, label, span, p {
                color: #FFFFFF !important;
            }
            /* Streamlit's widget labels */
            .css-16huue1, .css-1x8cf1d, .css-1vbd788, .css-12oz5g7, .stMarkdown {
                color: #FFFFFF !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            /* Light mode background and text */
            body, .main, .block-container {
                background-color: #FFFFFF !important;
                color: #000000 !important;
            }
            /* Input elements */
            textarea, input, .stRadio, .stSelectbox, .stTextArea {
                background-color: #f8f8f8 !important;
                color: #000000 !important;
            }
            /* Titles and text */
            h1, h2, h3, h4, h5, h6, label, span, p {
                color: #000000 !important;
            }
            /* Streamlit's widget labels */
            .css-16huue1, .css-1x8cf1d, .css-1vbd788, .css-12oz5g7, .stMarkdown {
                color: #000000 !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

###############################################################################
# 8. Streamlit App
###############################################################################
def main():
    st.set_page_config(page_title="CodeGenBot", layout="wide")

    # Create a top row with 2 columns: left for title, right for dark mode toggle
    col_title, col_toggle = st.columns([0.8, 0.2])
    with col_title:
        st.markdown("<h1 style='text-align: left;'>🚀 CodeGenBot: AI-Powered Coding Assistant</h1>", unsafe_allow_html=True)
    with col_toggle:
        dark_mode = st.checkbox("🌙 Dark Mode", value=False)
    # Inject the CSS for the chosen theme
    inject_custom_css(dark_mode)

    # Provide a quick help section for techniques
    with st.expander("About Prompting Techniques"):
        st.write("**Below are the available techniques and their plain-language descriptions:**")
        for t in valid_techniques:
            st.markdown(f"**{t}**: {technique_descriptions[t]}")

    # Initialize session states for the multi-step approach
    if "redrafts" not in st.session_state:
        st.session_state["redrafts"] = []
    if "chosen_technique" not in st.session_state:
        st.session_state["chosen_technique"] = None
    if "chosen_redraft" not in st.session_state:
        st.session_state["chosen_redraft"] = None

    st.subheader("Step 1: Enter your coding request")
    user_prompt = st.text_area("What do you want CodeGenBot to do?", value="", height=100)

    st.subheader("Step 2: Choose a prompting technique")
    chosen_technique = st.selectbox("Pick a technique:", options=["(Select)"] + valid_techniques)

    # Button: Generate 2-3 Redrafts
    if st.button("Generate Redrafts"):
        if not user_prompt.strip():
            st.warning("Please enter a coding request before generating redrafts.")
        elif chosen_technique == "(Select)":
            st.warning("Please select a prompting technique.")
        else:
            st.session_state["redrafts"] = generate_prompt_redrafts(user_prompt, chosen_technique)
            st.session_state["chosen_technique"] = chosen_technique
            st.session_state["chosen_redraft"] = None

    # If redrafts exist, show them with a radio button
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

            # Also add to conversation history for follow-ups
            add_message("user", {"code": user_prompt, "explanation": ""})
            add_message("assistant", result)

    ############################################################################
    # Follow-up Conversation Section
    ############################################################################
    st.write("---")
    st.header("Follow-up Conversation")
    followup_input = st.text_input("Ask a follow-up question or refine your request:")

    if st.button("Send Follow-up"):
        if followup_input.strip():
            # Add user follow-up to conversation
            add_message("user", {"code": followup_input, "explanation": ""})

            # Generate a code+explanation response
            conv_messages = chat_history()
            assistant_result = generate_followup_code(conv_messages, followup_input)
            add_message("assistant", assistant_result)
        else:
            st.warning("Please enter a follow-up question.")

    # Display conversation history (code+explanation) in chronological order
    for m in chat_history():
        if m["role"] == "user":
            st.markdown(f"**You:** {m['content']['code']}")
        else:
            code_part = m["content"].get("code", "")
            expl_part = m["content"].get("explanation", "")
            st.markdown("**CodeGenBot responded:**")
            st.code(code_part, language="python")
            st.markdown(f"**Explanation:** {expl_part}")

if __name__ == "__main__":
    main()
