import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def improve_resume(resume_text):

    prompt = f"""
You are an expert resume reviewer.

Candidate Resume:

{resume_text}

Tasks:

1. Identify weak resume statements.

2. Rewrite them professionally.

3. Use strong action verbs.

4. Quantify achievements whenever possible.

5. Make the resume ATS friendly.

Return:

### Improved Resume Suggestions

with bullet points.
"""

    response = client.models.generate_content(
        model="models/gemini-flash-lite-latest",
        contents=prompt
    )

    return response.text