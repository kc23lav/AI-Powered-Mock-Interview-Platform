from interview_engine import client

def generate_final_report(evaluations):

    prompt = f"""
    You are an expert hiring manager.

    These are interview evaluations:

    {evaluations}

    Generate:

    Overall Readiness Score: X/100

    Strengths:
    - point

    Weaknesses:
    - point

    Recommendation:
    Ready / Moderately Ready / Needs Improvement

    Keep it professional.
    """

    response = client.models.generate_content(
        model="models/gemini-flash-lite-latest",
        contents=prompt
    )

    return response.text