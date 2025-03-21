# CodeGenBot: AI-Powered Coding Assistant

**CodeGenBot** is a Streamlit-based AI chatbot that helps developers generate, explain, and refine code. It features:
- **Multi-step Prompt Engineering**: Enter your coding request → choose a technique → generate redrafts → finalize code.
- **Multiple Prompting Techniques**: Zero Shot, Few Shot, Chain-of-Thought, Least-to-Most, Self-Consistency, Reflective, Backtracking, and Verbalizer.
- **Dark/Light Mode**: Toggle a moon button in the top-right corner for dark theme.
- **Follow-up Conversation**: Continue chatting with the bot to refine or extend solutions—all responses are structured as valid JSON with `"code"` and `"explanation"` keys.

---

## Table of Contents
1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Installation & Setup](#installation--setup)  
4. [Usage](#usage)  
5. [Prompting Techniques](#prompting-techniques)  
6. [Repository Structure](#repository-structure)  
7. [License](#license)  
8. [Contributing](#contributing)  

---

## Project Overview

This project was originally built as part of an **Intro to LLM** lab assignment. It uses the **LangChain Google Generative AI** integration (`langchain_google_genai`) to interact with Gemini-1.5-flash. The Streamlit app provides a user-friendly interface for prompt engineering, code generation, and iterative refinement.

---

## Features

1. **Multi-step Prompting Flow**  
   - Users provide an initial coding request, choose a prompting technique, see multiple redrafted prompts, and pick one to finalize the solution.

2. **Dark/Light Mode**  
   - A “🌙 Dark Mode” toggle in the top-right corner lets you switch between dark mode (black background with white text) and light mode.

3. **Technique Descriptions**  
   - An expandable section explains each prompting technique in plain language, making it accessible to non-technical users.

4. **Follow-up Conversation**  
   - After the initial solution is generated, users can ask further questions or refine their requests. All responses are returned as valid JSON with `"code"` and `"explanation"`.

5. **Strict JSON Enforcement**  
   - Every response from CodeGenBot is enforced to follow a strict JSON structure for consistency and ease of parsing.

---

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/codegenbot.git
   cd codegenbot
