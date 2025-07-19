import os
from openai import OpenAI

def load_text(file_path: str) -> str:
    """Loads text from a given file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def build_prompt(resume: str, job: str) -> str:
    """Builds the prompt to send to the LLM."""
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
    """Sends the prompt to OpenAI and returns the response."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def main():
    resume = load_text("examples/resume.txt")
    job = load_text("examples/job_description.txt")
    prompt = build_prompt(resume, job)
    result = get_match_score(prompt)
    print("\n🔍 Match Result:\n")
    print(result)

if __name__ == "__main__":
    main()
