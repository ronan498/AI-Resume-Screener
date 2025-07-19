# AI Resume Screener

I built this as a quick project to get hands-on experience working with LLM APIs.  
Rather than just playing with chat interfaces, I wanted to explore a real-world use case — so I chose resume matching.

This tool compares a resume and a job description, and uses an OpenAI model (like GPT-3.5 or GPT-4) to return:
- A match score out of 100
- A short explanation of the fit

There's a simple Streamlit UI for interacting with it, and a command-line version for quick testing or automation.

---

## What it does

- Upload a resume and a job description (as `.txt` files)
- The model reads both and gives:
  - a match score (0–100)
  - a one-line explanation of how well they fit

---

## Run locally

Set your OpenAI API key first:

```bash
export OPENAI_API_KEY=your-api-key-here
```bash

Then launch the web app:

```bash
streamlit run app.py
