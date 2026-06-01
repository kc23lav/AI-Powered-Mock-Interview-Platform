from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(
    report_text,
    chart_file
):
    filename = "Interview_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI Interview Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )
    
    content.append(
    Paragraph(
        "Interview Performance Chart",
        styles["Heading2"]
    )
)

    content.append(
    Spacer(1, 10)
)

    content.append(
    Image(
        chart_file,
        width=400,
        height=250
    )
)

    content.append(
    Spacer(1, 20)
)

    for line in report_text.split("\n"):

        content.append(
            Paragraph(
                line,
                styles["BodyText"]
            )
        )

    doc.build(content)

    return filename