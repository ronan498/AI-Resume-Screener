import os
import streamlit as st
from openai import OpenAI

# --- Utility functions (reuse logic) ---

def load_text_from_upload(uploaded_file):
    if uploaded_file is not None:
        return uploaded_file.read().decode("utf-8")
    return ""

def build_prompt(resume: str, job: str) -> str:
    return f"""
You are a job matching assistant.

Rate how well this resume matches the job description from 0 to 100, and provide a short explanation.

Job Description:
{job}

Resume:
{resume}

Output format:
Score: <number>/100
Explanation: <1-2 sentences>
"""

def get_match_score(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "⚠️ OpenAI API key not found. Please set it as the environment variable 'OPENAI_API_KEY'."
    
    client = OpenAI(api_key=api_key)
    
    if os.getenv("MOCK_MODE") == "1":
        return "Score: 87/100\nExplanation: Strong match on NLP and deployment, minor gaps in cloud-specific tools."

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error from OpenAI API: {e}"

# --- Streamlit UI ---

st.set_page_config(page_title="AI Resume Screener", page_icon="🤖")
st.title("🤖 AI Resume Screener")
st.markdown("Upload a resume and job description to get an AI-generated match score and explanation.")

with st.sidebar:
    st.header("Settings")
    model = st.selectbox("Model", options=["gpt-3.5-turbo", "gpt-4", "gpt-4o"])
    st.caption("To use GPT-4/GPT-4o, make sure your API key has access.")

resume_file = st.file_uploader("Upload Resume (.txt)", type=["txt"])
job_file = st.file_uploader("Upload Job Description (.txt)", type=["txt"])

if st.button("Score Match"):
    resume_text = load_text_from_upload(resume_file)
    job_text = load_text_from_upload(job_file)

    if resume_text and job_text:
        prompt = build_prompt(resume_text, job_text)
        result = get_match_score(prompt, model)
        st.subheader("🔍 Match Result")
        st.code(result)
    else:
        st.warning("Please upload both a resume and a job description.")
