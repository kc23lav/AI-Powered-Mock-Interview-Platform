from interview_engine import client

def evaluate_answer(question, answer):

    prompt = f"""
    You are an expert technical interviewer.

    Question:
    {question}

    Candidate Answer:
    {answer}

    Evaluate the answer.

    Give:

    Score: X/10

    Feedback:
    2-3 lines

    Strengths:
    - point

    Improvements:
    - point
    """

    response = client.models.generate_content(
        model="models/gemini-flash-lite-latest",
        contents=prompt
    )

    return response.text