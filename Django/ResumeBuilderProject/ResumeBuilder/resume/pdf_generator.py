from io import BytesIO
from reportlab.platypus import Image,Spacer
from django.conf import settings
import os
from reportlab.lib.units import inch

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus import HRFlowable
from reportlab.lib import colors


def generate_resume(employee):

    # Create an in-memory buffer
    buffer = BytesIO()

    # Create PDF document
    doc = SimpleDocTemplate(
    buffer,
    topMargin=0.3 * inch,
    bottomMargin=0.5 * inch,
    leftMargin = 0.5 * inch,
    rightMargin = 0.5* inch
)

    # Default styles
    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.fontName = "Helvetica-Bold"
    title_style.fontSize = 22
    title_style.alignment = 1
    title_style.spaceAfter = 10

    designation_style = styles["Heading3"]
    designation_style.alignment = 1
    designation_style.spaceAfter = 20

    heading_style = styles["Heading2"]
    heading_style.fontName = "Helvetica-Bold"
    heading_style.fontSize = 14
    heading_style.spaceBefore = 12
    heading_style.spaceAfter = 8

    body_style = styles["BodyText"]
    body_style.fontName = "Helvetica"
    body_style.fontSize = 10
    body_style.leading = 18

    bullet_style = styles["BodyText"]
    bullet_style.leftIndent = 20
    bullet_style.leading = 16


    # List to store all PDF elements
    elements = []

    logo_path = os.path.join(
    settings.BASE_DIR,
    "resume",
    "static",
    "images",
    "logo.png"
)

    logo = Image(logo_path, width=600, height=50)
    logo.hAlign = "CENTER"

    elements.append(logo)

    elements.append(Spacer(1, 15))

    # =========================
    # Name
    # =========================
    elements.append(
        Paragraph(
            f"{employee.first_name} {employee.last_name}",
            title_style
        )
    )

    # =========================
    # Designation
    # =========================
    elements.append(
        Paragraph(
            employee.designation,
            designation_style
        )
    )

    # =========================
    # Professional Summary
    # =========================
    elements.append(
        Paragraph(
            "<b>Professional Summary</b>",
            heading_style
        )
    )

    elements.append(
        Paragraph(
            employee.summary,
            body_style
        )
    )

    # =========================
    # Technical Skills
    # =========================
    elements.append(
        Paragraph(
            "<b>Technical Skill Set</b>",
            heading_style
        )
    )

    skills = {}

    for skill in employee.skills.all():

        if skill.category not in skills:
            skills[skill.category] = []

        skills[skill.category].append(skill.skill)

    for category, skill_list in skills.items():

        elements.append(
            Paragraph(
                f"<b>{category}</b> : {', '.join(skill_list)}",
                body_style
            )
        )

    # =========================
    # Professional Projects
    # =========================
    elements.append(
        Paragraph(
            "<b>Professional Projects</b>",
            heading_style
        )
    )

    for index, employee_project in enumerate(
        employee.employee_projects.all(),
        start=1
    ):

        # Project Name
        elements.append(
            Paragraph(
                f"<b>Project {index}: {employee_project.project.project_name}</b>",
                heading_style
            )
        )

        # Technology Used
        elements.append(
            Paragraph(
                f"<b>Technology Used:</b> {employee_project.project.technology}",
                body_style
            )
        )

        # Description
        elements.append(
            Paragraph(
                f"<b>Description:</b> {employee_project.project.description}",
                body_style
            )
        )

        # Role
        elements.append(
            Paragraph(
                f"<b>Role:</b> {employee_project.role}",
                body_style
            )
        )

        # Responsibilities Heading
        elements.append(
            Paragraph(
                "<b>Responsibilities:</b>",
                body_style
            )
        )

        # Responsibilities
        for responsibility in employee_project.responsibilities.all():

            elements.append(
                Paragraph(
                    f"• {responsibility.responsibility}",
                    bullet_style
                )
            )

        elements.append(Spacer(1, 10))

        elements.append(
        HRFlowable(
        width="100%",
        thickness=1,
        color=colors.grey,
        spaceBefore=5,
        spaceAfter=10,
    )
)

        elements.append(Spacer(1, 10))

        # Blank line after every project
        elements.append(
            Paragraph(
                "<br/>",
                body_style
            )
        )

    # Build PDF
    doc.build(elements)

    # Move pointer to beginning
    buffer.seek(0)

    return buffer