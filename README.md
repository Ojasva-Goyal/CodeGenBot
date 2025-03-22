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
3. [Installation & Setup](#-installation--setup)  
4. [Usage](#-usage)  
5. [Prompting Techniques](#-prompting-techniques)  
6. [Repository Structure](#-repository-structure)  
7. [License](#-license)  
8. [Contributing](#-contributing)  

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

## 🚀 Installation & Setup

### 1. Clone the GitHub repository

```bash
git clone https://github.com/your-username/codegenbot.git
cd codegenbot
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your Google API key

#### Option A: Export it in your shell

```bash
export GOOGLE_API_KEY="YOUR_API_KEY_HERE"
```

#### Option B: The app will prompt you for your API key if it is not already set.

### 5. Run the Streamlit app

```bash
streamlit run streamlit_app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser to use CodeGenBot.

---

## 💡 Usage

1. **Enter your coding request:**  
   For example: “How do I write a function to reverse a list in Python?”

2. **Choose a prompting technique:**  
   Select one (e.g., Zero Shot, Few Shot, Chain-of-Thought, etc.) from the dropdown.

3. **Generate Redrafts:**  
   Click “Generate Redrafts” to view 2–3 rephrasings of your request with the selected technique.

4. **Pick a Redraft:**  
   Choose your preferred redrafted prompt using radio buttons.

5. **Generate Final Code:**  
   Click “Generate Final Code” to receive a JSON response containing:
   - `"code"`: displayed in a Python code block.
   - `"explanation"`: shown in plain text.

6. **Follow-up Conversation:**  
   Use this section to ask further questions or make refinements. CodeGenBot uses the context to generate responses.

7. **Dark/Light Mode:**  
   Use the “🌙 Dark Mode” checkbox at the top-right to toggle themes.

---

## 🧠 Prompting Techniques

Each technique adds a unique flavor to the model's response:

- **Zero Shot:** No examples provided—the model answers directly.
- **Few Shot:** A few examples guide the response format/style.
- **Chain-of-Thought:** The model "thinks aloud" step by step.
- **Least-to-Most:** Breaks the problem into smaller sub-problems.
- **Self-Consistency:** Generates multiple solutions and picks the most consistent one.
- **Reflective:** Generates an initial solution, then refines it.
- **Backtracking:** Corrects its initial answer by backtracking reasoning.
- **Verbalizer:** Structures the answer by explicitly verbalizing the reasoning.

---

## 📁 Repository Structure

```
codegenbot/
├── LICENSE
├── README.md
├── requirements.txt
├── .gitignore
├── streamlit_app.py         # Main entry point for the Streamlit app
└── notebooks/
    └── llm_lab_1.ipynb
└── src/
    ├── config.py            # LLM configuration, base prompts, and technique instructions/descriptions
    ├── prompts.py           # Functions for prompt redrafting and final code generation
    ├── utils.py             # Utility functions (e.g., conversation history management)
    ├── theme.py             # Functions to inject custom CSS for dark/light mode
    └── conversation.py      # Functions for handling follow-up conversation responses

```

- `streamlit_app.py`: Main Streamlit app with multi-step prompt flow.
- `requirements.txt`: Lists required Python packages.
- `LICENSE`: MIT License.
- `notebooks/llm_lab_1.ipynb`: Original lab notebook.

---

## 📜 License

This project is licensed under the MIT License. You are free to modify and distribute it as long as you include the original license.

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork this repository.
2. Create a new branch for your feature or fix.
3. Make your changes and test them.
4. Submit a Pull Request with a clear explanation.

---

## Contact
Created by `Ojasva Goyal` - feel free to contact me at ojasvagoyal9@gmail.com for any questions or feedback.

---

**Happy Coding! 💻✨**
