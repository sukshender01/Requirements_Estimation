import streamlit as st
import pandas as pd

def render_risks_and_mitigations(conf, features):
    st.subheader("📌 Risk Management & Assumptions")

    risks = [
        {"Risk": "Unclear requirements", "Impact": "High", "Mitigation": "Conduct clarification workshops"},
        {"Risk": "Underestimated complexity", "Impact": "Medium", "Mitigation": "Add buffer effort (20%)"},
        {"Risk": "Team skill gap", "Impact": "Medium", "Mitigation": "Provide training / hire experts"},
        {"Risk": "Scope creep", "Impact": "High", "Mitigation": "Strict change management"},
    ]

    df = pd.DataFrame(risks)

    st.markdown("### ✍️ Editable Risk Register")
    edited = st.data_editor(df, num_rows="dynamic")  # ✅ FIXED (no more experimental_ prefix)

    st.markdown("### ✅ Final Risks & Mitigations")
    st.dataframe(edited)

    return edited
