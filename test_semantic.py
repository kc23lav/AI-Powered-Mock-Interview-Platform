from semantic_matcher import semantic_match_score

resume = """
Java Developer
Spring Boot
REST API
MySQL
"""

jd = """
Backend Engineer

Requirements:
Java
Microservices
REST Services
SQL Databases
"""

score = semantic_match_score(
    resume,
    jd
)

print(score)