# app.py - main Streamlit app (root)
import sys, os
import streamlit as st

# Ensure local flat .py files are importable
sys.path.append(os.path.dirname(__file__))

from input_handler import get_requirements_text
from feature_extraction import extract_features
from assumptions import AssumptionsUI, load_default_assumptions
from estimators import run_selected_estimators, EstimationTechniquesList
from team_planner import plan_team_and_sprints
from charts import render_charts, create_gantt_figure
from export_utils import build_export_packages
from help_notes import render_help_notes
from risk_management import render_risks_and_mitigations


st.set_page_config(
    page_title="Effort Estimation Suite",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧮 Effort Estimation Suite — Modular (flat files)")

# Sidebar: techniques selection
with st.sidebar:
    st.header("Estimation Techniques")
    techniques = EstimationTechniquesList()
    selected = techniques.checkbox_selector()
    st.markdown("---")
    st.header("Assumptions")
    assumptions = AssumptionsUI()
    CONF = assumptions.render()  # returns dict of assumption values
    st.markdown("---")
    st.header("Help & Notes")
    render_help_notes()

# Input area (paste/upload)
requirements_text = get_requirements_text()

if not requirements_text.strip():
    st.info("Paste requirements or upload a document using the left control.")
    st.stop()

# Feature extraction
features = extract_features(requirements_text)
st.subheader("🔎 Identified Features")
st.table({"Feature (extracted)": features[:200]})

# Run estimators
estimation_results, per_feature_df = run_selected_estimators(
    techniques=selected,
    requirements_text=requirements_text,
    features=features,
    assumptions=CONF
)

st.subheader("📋 Estimation Summary (techniques)")
st.table(estimation_results)

st.subheader("📌 Per-feature breakdown (if AI/Agile used)")
if per_feature_df is not None and not per_feature_df.empty:
    st.dataframe(per_feature_df, use_container_width=True)

# Charts
st.subheader("📈 Visuals")
figs = render_charts(estimation_results, per_feature_df, CONF)
for title, fig in figs.items():
    st.markdown(f"**{title}**")
    st.pyplot(fig, use_container_width=True)

# Team & sprint planning
st.subheader("👥 Team Plan & Sprints")
team_plan = plan_team_and_sprints(estimation_results, assumptions=CONF, features=features)
st.table(team_plan)

# Risks & mitigations
st.subheader("⚠️ Risks, Assumptions & Mitigations")
render_risks_and_mitigations(CONF, features)

# Export & download area
st.subheader("📦 Export")
exports = build_export_packages(
    project_title="Effort Estimation Report",
    requirements_text=requirements_text,
    features=features,
    estimation_results=estimation_results,
    per_feature_df=per_feature_df,
    team_plan=team_plan,
    assumptions=CONF,
    figs=figs
)

col1, col2 = st.columns(2)
with col1:
    st.download_button(
        "⬇️ Download Excel (.xlsx)",
        exports["excel_bytes"],
        file_name="estimation_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
with col2:
    st.download_button(
        "⬇️ Download PDF (.pdf)",
        exports["pdf_bytes"],
        file_name="estimation_report.pdf",
        mime="application/pdf"
    )

st.success("Done — export buttons above provide single-click download (no double-click).")
