def calculate_match(resume_text, jd_text):

    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())

    matched = resume_words.intersection(jd_words)

    missing = jd_words - resume_words

    recommendations = []

    for skill in missing:

        if skill == "docker":
            recommendations.append(
                "Learn Docker Fundamentals"
            )

        elif skill == "aws":
            recommendations.append(
                "Learn AWS EC2 and S3 Basics"
            )

        elif skill == "mysql":
            recommendations.append(
                "Practice MySQL Queries and Joins"
            )

        elif skill == "java":
            recommendations.append(
                "Strengthen Java Core Concepts"
            )

        else:
            recommendations.append(
                f"Improve knowledge of {skill}"
            )

    if len(jd_words) == 0:
        return 0, [], [], []

    score = int(
        (len(matched) / len(jd_words)) * 100
    )

    return (
        score,
        list(matched),
        list(missing),
        recommendations
    )