import json
import re
from src.config import llm, BASE_SYSTEM_PROMPT, TECHNIQUE_INSTRUCTIONS

def extract_json_str(text: str) -> str:
    """Extract a JSON block from a text using regex."""
    match = re.search(r'\{.*\}', text, re.DOTALL)
    return match.group(0).strip() if match else ""

def parse_strict_json(raw_text: str) -> dict:
    """Parse text into strict JSON; fallback to regex extraction if needed."""
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        maybe_json = extract_json_str(raw_text)
        try:
            data = json.loads(maybe_json)
        except json.JSONDecodeError:
            data = {"code": "No valid JSON found in the response.", "explanation": raw_text}
    if "code" not in data:
        data["code"] = "No code returned."
    if "explanation" not in data:
        data["explanation"] = "No explanation returned."
    return data

def generate_prompt_redrafts(user_prompt: str, technique: str) -> list:
    """
    Generate 2-3 alternative rephrasings of the user's prompt based on the chosen technique.
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
    redrafts = []
    current = []
    for line in text.split("\n"):
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
    Generate final code and explanation based on the chosen redraft and technique.
    """
    technique_extra = TECHNIQUE_INSTRUCTIONS.get(technique, "")
    updated_prompt = (
        f"{BASE_SYSTEM_PROMPT}\n\nAdditional Technique Guidance:\n{technique_extra}"
        f"\n\nUser Request:\n{chosen_prompt}\n\nIMPORTANT: Return valid JSON only, with keys 'code' and 'explanation'."
    )
    response = llm.invoke(updated_prompt)
    raw_text = response.content if hasattr(response, "content") else str(response)
    return parse_strict_json(raw_text)
