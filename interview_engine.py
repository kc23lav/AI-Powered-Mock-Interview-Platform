import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_questions(resume_text, jd_text):

    prompt = f"""
    You are a professional technical interviewer.

    Candidate Resume:
    {resume_text}

    Job Description:
    {jd_text}

    Generate exactly 5 interview questions.

    Include:
    - Technical Questions
    - Conceptual Questions
    - Scenario Based Questions

    Return only the questions.
    """

    response = client.models.generate_content(
        model="models/gemini-flash-lite-latest",
        contents=prompt
    )

    questions = response.text.split("\n")

    clean_questions = []

    for q in questions:

        q = q.strip()

        if q:
            clean_questions.append(q)

    return clean_questions