import streamlit as st

def chat_history() -> list:
    """
    Get or initialize the conversation history stored in Streamlit's session state.
    """
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    return st.session_state["messages"]

def add_message(role: str, content: dict):
    """
    Add a new message (with role and content) to the conversation history.
    """
    history = chat_history()
    history.append({"role": role, "content": content})
