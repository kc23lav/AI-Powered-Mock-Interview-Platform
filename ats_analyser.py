TECH_SKILLS = [

    "java",
    "python",
    "mysql",
    "sql",
    "spring",
    "spring boot",
    "docker",
    "aws",
    "git",
    "github",
    "flask",
    "rest api",
    "rest",
    "microservices",
    "kafka",
    "rabbitmq",
    "junit",
    "react",
    "javascript",
    "html",
    "css"
]


def calculate_ats_score(
    resume_text,
    jd_text
):

    resume_text = resume_text.lower()

    jd_text = jd_text.lower()

    matched_skills = []

    missing_skills = []

    required_skills = []

    for skill in TECH_SKILLS:

        if skill in jd_text:

            required_skills.append(skill)

            if skill in resume_text:

                matched_skills.append(skill)

            else:

                missing_skills.append(skill)

    if len(required_skills) == 0:

        score = 0

    else:

        score = (
            len(matched_skills)
            /
            len(required_skills)
        ) * 100

    return {
        "score": round(score),
        "matched": matched_skills,
        "missing": missing_skills
    }