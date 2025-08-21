# risk_management.py
import streamlit as st
import pandas as pd

DEFAULT_RISKS = [
    {"Risk":"Unclear requirements","Category":"Scope","Likelihood":"High","Impact":"High","Mitigation":"Clarify via workshops, add spikes"},
    {"Risk":"Third-party API delays","Category":"Dependency","Likelihood":"Medium","Impact":"High","Mitigation":"Parallel integration tasks, fallbacks"},
    {"Risk":"Regulatory compliance","Category":"Compliance","Likelihood":"Low","Impact":"High","Mitigation":"Legal review early"}
]

def render_risks_and_mitigations(assumptions, features):
    st.markdown("**Assumptions used**")
    st.write(assumptions)
    st.markdown("**Risk register (editable)**")
    df = pd.DataFrame(DEFAULT_RISKS)
    edited = st.experimental_data_editor(df, num_rows="dynamic")
    st.markdown("**RACI for top risks (suggested)**")
    raci = {"Risk": [], "Responsible": [], "Accountable": [], "Consulted": [], "Informed": []}
    for r in edited["Risk"].head(3).tolist():
        raci["Risk"].append(r)
        raci["Responsible"].append("Dev Lead")
        raci["Accountable"].append("Project Manager")
        raci["Consulted"].append("Architect")
        raci["Informed"].append("Stakeholders")
    st.table(pd.DataFrame(raci))
