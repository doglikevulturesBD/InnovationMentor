
import streamlit as st
from utils.export import render_markdown

st.title("Export — Markdown (MVP)")
project_name = st.text_input("Project name", "Innovation Demo")
trl = st.session_state.get("trl_level","N/A")
top3 = st.session_state.get("top3_models", [])
finance = st.session_state.get("finance_snapshot", {})
marketing = st.session_state.get("marketing", {})
summary = {
    "project_name": project_name,
    "trl": trl,
    "top_models": [{"name": n, "why":"Fit from profile & TRL gate"} for n in top3],
    "finance": finance,
    "notes": f"Segment: {marketing.get('segment','-')}; Proposition: {marketing.get('value_prop','-')}; Pricing: {marketing.get('pricing','-')}; Channels: {marketing.get('channels','-')}"
}
md = render_markdown(summary)
st.download_button("Download Markdown Summary", data=md, file_name=f"{project_name.replace(' ','_')}_summary.md")
