import re


def extract_metrics(text):

    metrics = {}

    patterns = {
        "Technical Accuracy":
        r"Technical Accuracy:\s*(\d+)",

        "Communication":
        r"Communication:\s*(\d+)",

        "Problem Solving":
        r"Problem Solving:\s*(\d+)",

        "Confidence":
        r"Confidence:\s*(\d+)",

        "Overall Score":
        r"Overall Score:\s*(\d+\.?\d*)"
    }

    for key, pattern in patterns.items():

        match = re.search(
            pattern,
            text
        )

        if match:

            metrics[key] = float(
                match.group(1)
            )

    return metrics