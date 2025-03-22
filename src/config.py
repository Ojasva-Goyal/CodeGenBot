import os
import getpass
from langchain_google_genai import ChatGoogleGenerativeAI

# Ensure the Google API Key is set
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

# Configure the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

# Base system prompt with strict JSON requirement
BASE_SYSTEM_PROMPT = """
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

# Technique instructions and descriptions
TECHNIQUE_INSTRUCTIONS = {
    "zero_shot": "Answer directly with minimal additional context.",
    "few_shot": "Provide 1-2 brief examples before giving your main solution.",
    "chain_of_thought": "Think aloud step-by-step before finalizing the solution.",
    "least_to_most": "Break the problem into smaller sub-problems and solve them in order.",
    "self_consistency": "Generate multiple reasoning paths internally, then pick the most consistent.",
    "reflective": "Present an initial solution, then reflect and refine your answer.",
    "backtracking": "Propose a solution, then backtrack to correct mistakes or inefficiencies.",
    "verbalizer": "Explicitly verbalize the reasoning and structure the final answer clearly."
}

TECHNIQUE_DESCRIPTIONS = {
    "zero_shot": "No examples are provided—the model responds solely based on its internal knowledge.",
    "few_shot": "A few examples are given to guide the format and style of the answer.",
    "chain_of_thought": "The model 'thinks aloud', showing step-by-step reasoning before the final answer.",
    "least_to_most": "The problem is broken into smaller steps and solved sequentially.",
    "self_consistency": "Multiple solution paths are generated internally and the most consistent is chosen.",
    "reflective": "An initial solution is provided, then refined after reflection.",
    "backtracking": "The model corrects its first answer by backtracking and optimizing the solution.",
    "verbalizer": "The model explicitly explains its reasoning process in detail."
}

VALID_TECHNIQUES = list(TECHNIQUE_INSTRUCTIONS.keys())
