import json
import re
from src.config import BASE_SYSTEM_PROMPT
from src.config import llm
from src.prompts import parse_strict_json

def generate_followup_code(conversation_messages: list, user_message: str) -> dict:
    """
    Generate a follow-up code response based on conversation history and the new user message.
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
        f"{BASE_SYSTEM_PROMPT}\n\nHere is the conversation so far:\n{conversation_text}\n"
        f"Now the user says:\n{user_message}\n\nIMPORTANT: Return valid JSON only, with keys 'code' and 'explanation'."
    )
    response = llm.invoke(followup_prompt)
    raw_text = response.content if hasattr(response, "content") else str(response)
    return parse_strict_json(raw_text)
