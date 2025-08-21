# assumptions.py
import streamlit as st

def load_default_assumptions():
    return {
        "avg_loc_per_feature": 200,
        "cocomo_mode": "organic",
        "fp_vaf": 1.0,
        "fp_hours_per_fp": 8.0,
        "ucp_tcf": 0.9,
        "ucp_ef": 1.1,
        "ucp_hours_per_ucp": 20.0,
        "hours_per_sp": 8.0
    }

class AssumptionsUI:
    def render(self):
        defaults = load_default_assumptions()
        st.subheader("Estimation assumptions (editable)")
        a1 = st.number_input("Avg LOC per feature (COCOMO)", value=int(defaults["avg_loc_per_feature"]), step=10, key="a_loc")
        mode = st.selectbox("COCOMO mode", options=["organic","semi-detached","embedded"], index=0, key="a_mode")
        fp_vaf = st.slider("FP VAF", 0.6, 1.4, value=float(defaults["fp_vaf"]), key="a_vaf")
        fp_hpf = st.number_input("Hours per FP", value=float(defaults["fp_hours_per_fp"]), step=0.5, key="a_hpf")
        ucp_tcf = st.slider("UCP TCF", 0.6, 1.4, value=float(defaults["ucp_tcf"]), key="a_tcf")
        ucp_ef = st.slider("UCP EF", 0.6, 1.4, value=float(defaults["ucp_ef"]), key="a_ef")
        ucp_h = st.number_input("Hours per UCP", value=float(defaults["ucp_hours_per_ucp"]), step=1.0, key="a_ucp_h")
        h_per_sp = st.number_input("Hours per Story Point", value=float(defaults["hours_per_sp"]), step=0.5, key="a_hsp")
        return {
            "avg_loc_per_feature": a1,
            "cocomo_mode": mode,
            "fp_vaf": fp_vaf,
            "fp_hours_per_fp": fp_hpf,
            "ucp_tcf": ucp_tcf,
            "ucp_ef": ucp_ef,
            "ucp_hours_per_ucp": ucp_h,
            "hours_per_sp": h_per_sp
        }
