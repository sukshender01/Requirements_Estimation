# estimators.py
import pandas as pd
import math
from typing import List, Dict, Tuple

# Enumerate available techniques
def EstimationTechniquesList():
    # returns object with checkbox_selector method that renders checkbox UI
    class _T:
        def checkbox_selector(self):
            import streamlit as st
            st.write("Pick techniques (one or many):")
            choices = {
                "COCOMO": st.checkbox("COCOMO (basic)", value=True, key="cb_cocomo"),
                "Function Points": st.checkbox("Function Points (FP)", value=True, key="cb_fp"),
                "Use Case Points": st.checkbox("Use Case Points (UCP)", value=True, key="cb_ucp"),
                "Story Points": st.checkbox("Story Point / Agile", value=True, key="cb_story"),
                "AI NLP": st.checkbox("AI-based NLP estimate (heuristic)", value=False, key="cb_ai")
            }
            selected = [k for k,v in choices.items() if v]
            return selected
    return _T()

# --- Individual estimator implementations (simple but defensible formulas) ---
def cocomo_estimate(features: List[str], avg_loc_per_feature:int=200, mode="organic") -> Dict:
    # Basic COCOMO (81) approximation via KLOC -> effort PM (a*kloc^b)
    loc = max(1, avg_loc_per_feature) * max(1, len(features))
    kloc = loc / 1000.0
    params = {"organic":(2.4,1.05), "semi-detached":(3.0,1.12), "embedded":(3.6,1.20)}
    a,b = params.get(mode, params["organic"])
    pm = a * (kloc ** b)
    hours = pm * 152  # ~19 working days * 8h
    return {"technique":"COCOMO","KLOC":round(kloc,3),"PM":round(pm,2),"Hours":round(hours,1)}

def function_points_estimate(features: List[str], vaf:float=1.0, hours_per_fp:float=8.0) -> Dict:
    # Simplified UFP derivation: each feature ~ 4 FP average
    ufp = max(1, len(features)) * 4.0
    fp = ufp * vaf
    hours = fp * hours_per_fp
    return {"technique":"Function Points","UFP":round(ufp,1),"FP":round(fp,1),"Hours":round(hours,1)}

def use_case_points_estimate(features: List[str], tcf:float=0.9, ef:float=1.1, hours_per_ucp:float=20.0) -> Dict:
    # Basic UCP: UUCW approx = #features * 4; UAW assume 3
    uucw = len(features) * 4
    uaw = 3
    ucp = (uucw + uaw) * tcf * ef
    hours = ucp * hours_per_ucp
    return {"technique":"Use Case Points","UUCW":uucw,"UAW":uaw,"UCP":round(ucp,1),"Hours":round(hours,1)}

def story_points_estimate(features: List[str], hours_per_sp:float=8.0) -> Dict:
    # Map: simple:2, medium:5, complex:8 -> heuristics based on text length
    sp = 0
    for f in features:
        L = len(f)
        if L < 40:
            sp += 2
        elif L < 120:
            sp += 5
        else:
            sp += 8
    hours = sp * hours_per_sp
    return {"technique":"Story Points","StoryPoints":int(sp),"Hours":round(hours,1)}

def ai_nlp_estimate(requirements_text:str) -> Dict:
    # Heuristic AI fallback: word count -> hours
    words = len(requirements_text.split())
    hours = words * 0.08  # 0.08 hours per word ~ 5 words/hour mapping (tunable)
    return {"technique":"AI-NLP (heuristic)","Words":words,"Hours":round(hours,1)}

# Main runner
def run_selected_estimators(techniques: List[str], requirements_text: str, features: List[str], assumptions: Dict) -> Tuple[pd.DataFrame, pd.DataFrame]:
    results = []
    per_feature_rows = []
    # COCOMO
    if "COCOMO" in techniques:
        coco = cocomo_estimate(features, avg_loc_per_feature=int(assumptions.get("avg_loc_per_feature",200)), mode=assumptions.get("cocomo_mode","organic"))
        results.append({"Technique":coco["technique"], "Hours":coco["Hours"], "Notes":f"KLOC={coco['KLOC']} PM={coco['PM']}"})
    if "Function Points" in techniques:
        fp = function_points_estimate(features, vaf=float(assumptions.get("fp_vaf",1.0)), hours_per_fp=float(assumptions.get("fp_hours_per_fp",8.0)))
        results.append({"Technique":fp["technique"], "Hours":fp["Hours"], "Notes":f"UFP={fp['UFP']} FP={fp['FP']}"})
    if "Use Case Points" in techniques:
        ucp = use_case_points_estimate(features, tcf=float(assumptions.get("ucp_tcf",0.9)), ef=float(assumptions.get("ucp_ef",1.1)), hours_per_ucp=float(assumptions.get("ucp_hours_per_ucp",20.0)))
        results.append({"Technique":ucp["technique"], "Hours":ucp["Hours"], "Notes":f"UCP={ucp['UCP']}"})
    if "Story Points" in techniques:
        sp = story_points_estimate(features, hours_per_sp=float(assumptions.get("hours_per_sp",8.0)))
        results.append({"Technique":sp["technique"], "Hours":sp["Hours"], "Notes":f"SP={sp['StoryPoints']}"})
        # also per-feature SP mapping
        # naive mapping: short->2, medium->5, long->8
        for f in features:
            L = len(f)
            spv = 2 if L < 40 else 5 if L < 120 else 8
            per_feature_rows.append({"Feature":f,"SP":spv,"Hours":spv*float(assumptions.get("hours_per_sp",8.0))})
    if "AI-NLP" in techniques:
        ai = ai_nlp_estimate(requirements_text)
        results.append({"Technique":ai["technique"], "Hours":ai["Hours"], "Notes":f"Words={ai['Words']}"})
        # per-feature approximate split by ratio
        if len(features):
            per = ai["Hours"] / len(features)
            for f in features:
                per_feature_rows.append({"Feature":f,"SP":None,"Hours":round(per,2)})
    df_results = pd.DataFrame(results)
    per_feature_df = pd.DataFrame(per_feature_rows) if per_feature_rows else pd.DataFrame()
    return df_results, per_feature_df
