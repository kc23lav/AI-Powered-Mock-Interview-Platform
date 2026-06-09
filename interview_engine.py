import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_questions(resume_text, jd_text):

    prompt = f"""
You are a Senior Technical Interviewer at Google, Amazon, Microsoft, and Tesla.

Your task is to conduct a realistic interview based on the candidate's resume and the target job description.

Candidate Resume:
{resume_text}

Job Description:
{jd_text}

INSTRUCTIONS:

1. Carefully analyze:
   - Projects
   - Technical skills
   - Tools & technologies
   - Experience level
   - Missing skills compared to the JD

2. Generate EXACTLY 5 highly personalized interview questions.

Question Structure:

Question 1:
Project Deep Dive
- Ask about a major project from the resume.
- Focus on architecture, implementation, or technical decisions.

Question 2:
Technical Depth
- Ask about a key technology mentioned in the resume.
- Focus on concepts, trade-offs, or real implementation.

Question 3:
JD Gap Question
- Identify an important skill required in the JD but weak or missing in the resume.
- Ask a practical interview question on that topic.

Question 4:
Scenario / Problem Solving
- Create a realistic workplace scenario.
- Test debugging, design thinking, optimization, or decision making.

Question 5:
Scaling & System Design
- Take one project from the resume.
- Ask how it would be scaled to support thousands or millions of users.

IMPORTANT:

- Questions must feel like a real interviewer.
- Avoid definitions.
- Avoid theory-only questions.
- Focus on WHY, HOW, TRADE-OFFS, and DESIGN DECISIONS.
- Make every question unique.
- Questions should become progressively harder.

Return ONLY the 5 questions.
Do not include explanations.
Do not include headings.
Do not include bullet points.
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