import streamlit as st
from utils.export import render_markdown

st.set_page_config(page_title="Export Summary", layout="centered")

st.title("📄 Export — Markdown Summary (MVP)")
st.markdown("Generate a portable summary of your project using all key outputs captured across the tool.")

# -------------------------
# Gather context from session state
# -------------------------
project_name = st.text_input("Project name", "Innovation Demo")

trl = st.session_state.get("trl_level", "Not completed")
top3_models = st.session_state.get("top3_models", [])
finance = st.session_state.get("finance_snapshot", {})
marketing = st.session_state.get("marketing", {})

# Fallback label for business models
if isinstance(top3_models, dict):
    top3_models = list(top3_models.values())
if isinstance(top3_models, str):
    top3_models = [top3_models]

# -------------------------
# Build summary object
# -------------------------
summary = {
    "project_name": project_name,
    "trl": trl,
    "top_models": [
        {"name": model_name, "why": "Fit from profile & TRL gate"}
        for model_name in top3_models
    ] if top3_models else "No business model assessment completed.",
    "finance": finance if finance else "Finance module not completed.",
    "notes": (
        f"Segment: {marketing.get('segment','-')} | "
        f"Proposition: {marketing.get('value_prop','-')} | "
        f"Pricing: {marketing.get('pricing','-')} | "
        f"Channels: {marketing.get('channels','-')}"
    )
}

# -------------------------
# Generate Markdown using your utils.export renderer
# -------------------------
md = render_markdown(summary)

# -------------------------
# Download Button
# -------------------------
st.download_button(
    "⬇ Download Markdown Summary",
    data=md,
    file_name=f"{project_name.replace(' ','_')}_summary.md",
    mime="text/markdown"
)

# Optional preview
st.markdown("---")
with st.expander("📄 Preview Markdown Output"):
    st.code(md, language="markdown")

st.caption("This is a lightweight export. Full reports (PDF/Slides) will be available in a later version.")
