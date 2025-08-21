# charts.py
import matplotlib.pyplot as plt
import io
from typing import Dict
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime, timedelta

def render_charts(estimation_df, per_feature_df, assumptions):
    figs = {}
    # Technique comparison bar
    if estimation_df is not None and not estimation_df.empty:
        fig1, ax1 = plt.subplots()
        ax1.bar(estimation_df["Technique"], estimation_df["Hours"])
        ax1.set_ylabel("Estimated Hours")
        ax1.set_title("Technique Comparison")
        figs["Technique Comparison"] = fig1
    # Per-feature top N pie or bar
    if per_feature_df is not None and not per_feature_df.empty:
        top = per_feature_df.sort_values("Hours", ascending=False).head(10)
        fig2, ax2 = plt.subplots()
        ax2.pie(top["Hours"], labels=top["Feature"].str.slice(0,30), autopct="%1.1f%%")
        ax2.set_title("Top features by estimated hours")
        figs["Top features"] = fig2
    return figs

def create_gantt_figure(team_plan, num_sprints=4):
    # simple gantt: each sprint as block
    fig, ax = plt.subplots(figsize=(10,3))
    start = datetime.today()
    for i in range(num_sprints):
        ax.barh("Project", (10), left=start + timedelta(days=i*10), height=0.5)
    ax.set_title("Gantt (sprints view)")
    return fig

def fig_to_png_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=200)
    buf.seek(0)
    return buf.getvalue()
