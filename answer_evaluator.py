from interview_engine import client

def evaluate_answer(question, answer):

    prompt = f"""
You are an expert technical interviewer.

Evaluate the candidate's answer on the following dimensions:

1. Technical Accuracy (0-100)
2. Communication Skills (0-100)
3. Problem Solving Ability (0-100)
4. Confidence Level (0-100)

Then calculate:

Overall Score (0-100)

Question:
{question}

Answer:
{answer}

Return in this exact format:

Technical Accuracy: XX

Communication: XX

Problem Solving: XX

Confidence: XX

Overall Score: XX

Strengths:
- ...

Areas for Improvement:
- ...

Detailed Feedback:
...
"""

    response = client.models.generate_content(
        model="models/gemini-flash-lite-latest",
        contents=prompt
    )

    return response.text