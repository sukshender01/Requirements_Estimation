from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io

def build_pdf_bytes(project_title, narrative, sheets, figs_bytes):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)

    story = []
    styles = getSampleStyleSheet()

    # Title
    story.append(Paragraph(f"<b>{project_title}</b>", styles["Title"]))
    story.append(Spacer(1, 12))

    # Narrative
    story.append(Paragraph("Project Overview", styles["Heading2"]))
    story.append(Paragraph(narrative, styles["Normal"]))
    story.append(Spacer(1, 12))

    # Tables for each sheet
    for sheet_name, df in sheets.items():
        story.append(Paragraph(f"{sheet_name}", styles["Heading2"]))
        if df is not None and not df.empty:
            data = [df.columns.tolist()] + df.values.tolist()
            table = Table(data, repeatRows=1)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ]
                )
            )
            story.append(table)
        else:
            story.append(Paragraph("<i>No data available</i>", styles["Normal"]))
        story.append(Spacer(1, 12))

    # Figures
    if figs_bytes:
        from reportlab.platypus import Image
        for fig_bytes in figs_bytes:
            img = Image(io.BytesIO(fig_bytes))
            img._restrictSize(400, 300)
            story.append(img)
            story.append(Spacer(1, 12))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
