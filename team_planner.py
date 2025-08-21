# team_planner.py
import pandas as pd
import math

def plan_team_and_sprints(estimation_df, assumptions:dict, features:list):
    # compute average hours across selected techniques
    if estimation_df is None or estimation_df.empty:
        return pd.DataFrame()
    avg_hours = float(estimation_df["Hours"].mean())
    # naive team sizing: 1 dev = 120 hours/month (approx 3 weeks)
    months = max(1, math.ceil(avg_hours / 120.0))
    suggested_team = max(2, int(math.ceil(avg_hours / (8*20))))  # each dev 160h/month
    sprint_length_days = 10  # default
    sprint_capacity_per_dev = 8* sprint_length_days  # hours per sprint per dev
    sprints = max(1, int(math.ceil(avg_hours / (suggested_team * sprint_capacity_per_dev))))
    # role breakdown (simple percentages)
    roles = {"Dev":0.6, "QA":0.2, "BA":0.1, "PM":0.1}
    role_alloc = {r: max(1, int(math.ceil(suggested_team * pct))) for r,pct in roles.items()}
    plan = {
        "AvgEstimatedHours": round(avg_hours,1),
        "SuggestedTeamSize": suggested_team,
        "EstimatedMonths": months,
        "SprintLength(days)": sprint_length_days,
        "SuggestedSprints": sprints
    }
    table = pd.DataFrame.from_dict([plan])
    role_table = pd.DataFrame([role_alloc])
    # Return combined table view by concatenation
    return pd.concat([table, role_table], axis=1)
