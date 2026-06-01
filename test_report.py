from report_generator import generate_final_report

evaluations = """
Question 1:
Score: 6/10
Strengths:
- Good understanding of REST APIs

Improvements:
- Mention resource-based architecture

Question 2:
Score: 8/10
Strengths:
- Good Docker knowledge

Improvements:
- Explain container networking
"""

report = generate_final_report(
    evaluations
)

print(report)