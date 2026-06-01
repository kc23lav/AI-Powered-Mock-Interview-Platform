from interview_engine import generate_questions

resume = """
Python
Java
Flask
Machine Learning
"""

jd = """
Backend Developer
Java
MySQL
Docker
REST API
"""

print(generate_questions(resume, jd))