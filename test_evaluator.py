from answer_evaluator import evaluate_answer

question = "What is REST API?"

answer = """
REST API is an API that follows REST architecture.
It uses HTTP methods such as GET, POST, PUT and DELETE.
REST APIs are stateless and are commonly used for communication between client and server.
"""

result = evaluate_answer(
    question,
    answer
)

print(result)