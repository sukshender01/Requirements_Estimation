# export_utils.py
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from charts import fig_to_png_bytes, create_gantt_figure
from typing import Dict

def build_excel_bytes(sheets: Dict[str, pd.DataFrame]) -> bytes:
    wb = Workbook()
    # remove default sheet
    ws0 = wb.active
    wb.remove(ws0)
    for name, df in sheets.items():
        ws = wb.create_sheet(title=name[:31])
        for r in dataframe_to_rows(df, index=False, header=True):
            ws.append(r)
    bio = io.BytesIO()
    wb.save(bio)
    return bio.getvalue()

def build_pdf_bytes(title:str, narrative:str, sheets:Dict[str,pd.DataFrame], figs:Dict[str,bytes]) -> bytes:
    bio = io.BytesIO()
    doc = SimpleDocTemplate(bio, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph(title, styles['Title']))
    story.append(Spacer(1,12))
    story.append(Paragraph(narrative, styles['Normal']))
    story.append(Spacer(1,12))
    for name, df in sheets.items():
        story.append(Paragraph(name, styles['Heading2']))
        data = [list(df.columns)] + df.values.tolist()
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.lightgrey)]))
        story.append(table)
        story.append(Spacer(1,12))
    for title, figbytes in figs.items():
        story.append(Paragraph(title, styles['Heading3']))
        story.append(Spacer(1,6))
        img = Image(io.BytesIO(figbytes))
        img._restrictSize(480, 240)
        story.append(img)
        story.append(Spacer(1,10))
    doc.build(story)
    return bio.getvalue()

def build_export_packages(project_title, requirements_text, features, estimation_results, per_feature_df, team_plan, assumptions, figs):
    # Prepare sheets
    sheets = {}
    sheets["Estimation Summary"] = estimation_results if estimation_results is not None else pd.DataFrame()
    sheets["Per Feature"] = per_feature_df if per_feature_df is not None else pd.DataFrame()
    sheets["Team Plan"] = team_plan if team_plan is not None else pd.DataFrame()
    sheets["Assumptions"] = pd.DataFrame([assumptions])
    # Excel bytes
    excel_bytes = build_excel_bytes(sheets)
    # Prepare narrative and figs (convert matplotlib figs to bytes)
    figs_bytes = {}
    for k,v in figs.items():
        try:
            figs_bytes[k] = fig_to_png_bytes(v)
        except Exception:
            pass
    # Gantt
    try:
        gantt = create_gantt_figure(team_plan)
        figs_bytes["Gantt"] = fig_to_png_bytes(gantt)
    except Exception:
        pass
    narrative = f"Requirements excerpt:\n{(requirements_text[:800] + '...') if len(requirements_text)>800 else requirements_text}"
    pdf_bytes = build_pdf_bytes(project_title, narrative, sheets, figs_bytes)
    return {"excel_bytes":excel_bytes, "pdf_bytes":pdf_bytes}
