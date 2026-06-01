import re

def extract_scores(evaluations):

    scores = []

    for evaluation in evaluations:

        match = re.search(
            r"Score:\s*(\d+)/10",
            evaluation
        )

        if match:

            scores.append(
                int(match.group(1))
            )

    return scores