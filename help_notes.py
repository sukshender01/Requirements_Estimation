# help_notes.py
import streamlit as st

def render_help_notes():
    with st.expander("Help: Estimation Methods & Examples", expanded=False):
        st.markdown("**COCOMO (Basic)**\n\nFormula: PM = a * (KLOC^b). Example: KLOC=5, PM~2.4*5^1.05 ...")
        st.markdown("**Function Points**\n\nUFP estimated from features. Example: 10 features -> UFP=40 -> Hours = FP*hours_per_fp.")
        st.markdown("**Use Case Points**\n\nUCP = (UUCW+UAW)*TCF*EF. Example included in UI.")
        st.markdown("**Story Points**\n\nMap feature size to SP, use team velocity to convert to sprints.")
        st.markdown("**AI NLP**\n\nHeuristic fallback: word-count / semantics. Replace by external model (HuggingFace/Cohere) if desired.")
