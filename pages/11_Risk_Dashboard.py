# ============================================
# INNOVATION MENTOR APP
# PAGE: 07_Risk_Dashboard.py
# FUNCTION: Hybrid Dynamic Risk Dashboard
# ============================================

import json
from pathlib import Path
from collections import defaultdict
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Risk Dashboard")
st.title("Innovation Risk Dashboard")

st.markdown("""
This dashboard identifies your **Top Risks** by combining a short diagnostic questionnaire
with context from other modules (TRL, Business Model, IP, Funding, Marketing, Commercialisation).
It then suggests **practical mitigations** and lets you download a mini **Risk Register**.
---
""")

# ----------------------------
# Load JSON assets
# ----------------------------
def load_json(path: str):
    p = Path(path)
    if not p.exists():
        st.error(f"Missing file: {path}")
        st.stop()
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

engine = load_json("data/risk_engine.json")
library = load_json("data/risk_library.json")

weighting_rules = engine.get("weighting_rules", [])
questions = engine.get("questionnaire", [])
base_points_per_hit = engine.get("scoring", {}).get("base_points_per_hit", 10)
top_n = engine.get("scoring", {}).get("top_n", 5)

# ----------------------------
# Read context from session_state (safe defaults)
# These can be set by your other pages when users complete them.
# ----------------------------
trl_level = st.session_state.get("trl_level", 6)  # int 1-9
business_model = st.session_state.get("selected_business_model", None)  # e.g., "Licensing"
funding_stage = st.session_state.get("funding_stage", "Seed")  # e.g., "Pre-seed", "Seed", "Series A"
marketing_strategies = st.session_state.get("marketing_top_strategies", [])  # list[str]
commercialisation_pathway = st.session_state.get("commercialisation_pathway", None)  # e.g., "Public-Private Pilot"

with st.expander("ℹ️ Context detected from other modules (you can leave as-is):", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("TRL level", min_value=1, max_value=9, value=int(trl_level), key="ctx_trl")
        st.selectbox("Funding stage", ["Pre-seed", "Seed", "Series A", "Series B", "Revenue"], index=1 if funding_stage not in ["Pre-seed","Seed","Series A","Series B","Revenue"] else ["Pre-seed","Seed","Series A","Series B","Revenue"].index(funding_stage), key="ctx_funding")
    with col2:
        st.selectbox("Business model", ["Licensing", "Direct Sales", "Subscription", "Franchising / Replication Model", "Marketplace", "Other"], index=0 if business_model is None else  ["Licensing","Direct Sales","Subscription","Franchising / Replication Model","Marketplace","Other"].index(business_model) if business_model in ["Licensing","Direct Sales","Subscription","Franchising / Replication Model","Marketplace","Other"] else 5, key="ctx_bm")
        st.selectbox("Commercialisation pathway", ["Public-Private Pilot", "Direct Sales", "Licensing", "Joint Venture / Strategic Partnership", "Franchising / Replication Model", "Digital Platform / Ecosystem Integration", "Open-Innovation / Co-Development", "Unknown"], index=7 if commercialisation_pathway is None else ["Public-Private Pilot","Direct Sales","Licensing","Joint Venture / Strategic Partnership","Franchising / Replication Model","Digital Platform / Ecosystem Integration","Open-Innovation / Co-Development","Unknown"].index(commercialisation_pathway) if commercialisation_pathway in ["Public-Private Pilot","Direct Sales","Licensing","Joint Venture / Strategic Partnership","Franchising / Replication Model","Digital Platform / Ecosystem Integration","Open-Innovation / Co-Development","Unknown"] else 7, key="ctx_comm")
    with col3:
        st.multiselect(
            "Top marketing strategies",
            ["Product Differentiation", "Cost / Value Leadership", "Niche / Community Focus", "Partnership & Co-Creation", "Experience & Engagement", "Digital-First / Data-Driven", "Impact-First Branding", "Community-Powered Growth", "Ecosystem Storytelling"],
            default=marketing_strategies if marketing_strategies else []
            , key="ctx_mkt"
        )

# ----------------------------
# Questionnaire (6 Q)
# ----------------------------
st.subheader("🧭 Quick Risk Questionnaire")

base_scores = defaultdict(int)
answers = {}

for q in questions:
    st.markdown(f"**{q['question']}**")
    opts = [o["text"] for o in q["options"]]
    choice = st.radio("", opts, key=f"risk_q_{q['id']}")
    answers[q["id"]] = choice

    # Tally base hits
    selected = next(o for o in q["options"] if o["text"] == choice)
    for risk_type in selected.get("adds", []):
        base_scores[risk_type] += base_points_per_hit

    st.divider()

# ----------------------------
# Apply context-based weighting rules
# ----------------------------
ctx = {
    "trl": int(st.session_state["ctx_trl"]),
    "business_model": st.session_state["ctx_bm"],
    "funding_stage": st.session_state["ctx_funding"],
    "marketing": set(st.session_state["ctx_mkt"]),
    "commercialisation": st.session_state["ctx_comm"]
}

weighted_scores = defaultdict(int, base_scores)

def rule_matches(rule_when: dict) -> bool:
    # TRL rule
    trl_max = rule_when.get("trl_max", None)
    if trl_max is not None and ctx["trl"] > int(trl_max):
        return False

    # Business model inclusion
    bm_any = rule_when.get("business_model_any", None)
    if bm_any and ctx["business_model"] not in bm_any:
        return False

    # Funding stage inclusion
    fs_any = rule_when.get("funding_stage_any", None)
    if fs_any and ctx["funding_stage"] not in fs_any:
        return False

    # Marketing strategies inclusion (any)
    mkt_any = rule_when.get("marketing_any", None)
    if mkt_any and not (set(mkt_any) & ctx["marketing"]):
        return False

    # Commercialisation pathway inclusion (any)
    comm_any = rule_when.get("commercialisation_any", None)
    if comm_any and ctx["commercialisation"] not in comm_any:
        return False

    return True

for rule in weighting_rules:
    if rule_matches(rule.get("when", {})):
        for risk_type, bonus in rule.get("weights", {}).items():
            weighted_scores[risk_type] += int(bonus)

# ----------------------------
# Produce Top-N list and visual
# ----------------------------
sorted_risks = sorted(weighted_scores.items(), key=lambda x: x[1], reverse=True)
top_risks = [(r, s) for r, s in sorted_risks if s > 0][:top_n]

st.subheader("📊 Top Risks")
if not top_risks:
    st.info("No material risks identified yet. Adjust your answers or context.")
else:
    # Chart
    chart_df = pd.DataFrame(top_risks, columns=["Risk", "Score"]).set_index("Risk")
    st.bar_chart(chart_df)

    st.markdown("---")
    # Detail cards
    for risk_type, score in top_risks:
        data = library.get(risk_type, {})
        with st.expander(f"{risk_type} — Score {score}"):
            st.markdown(f"**Description:** {data.get('description', '—')}")
            ind = data.get("indicators", [])
            if ind:
                st.markdown("**Indicators:**")
                for i in ind:
                    st.markdown(f"- {i}")
            mit = data.get("mitigation", [])
            if mit:
                st.markdown("**Mitigation suggestions:**")
                for m in mit:
                    st.markdown(f"- {m}")
            st.markdown(f"**Severity (library baseline):** {data.get('severity', '—')}")

# ----------------------------
# Downloadable Risk Register (CSV)
# ----------------------------
if top_risks:
    rows = []
    for risk_type, score in top_risks:
        e = library.get(risk_type, {})
        rows.append({
            "Risk": risk_type,
            "Score": score,
            "Severity (baseline)": e.get("severity", ""),
            "Description": e.get("description", ""),
            "Top Mitigation #1": (e.get("mitigation", ["", "", ""]) + ["", "", ""])[0],
            "Top Mitigation #2": (e.get("mitigation", ["", "", ""]) + ["", "", ""])[1],
            "Top Mitigation #3": (e.get("mitigation", ["", "", ""]) + ["", "", ""])[2]
        })
    df = pd.DataFrame(rows)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Risk Register (CSV)", csv, file_name="risk_register.csv", mime="text/csv")

st.caption("Tip: Other pages can set session_state keys like trl_level, selected_business_model, funding_stage, marketing_top_strategies, commercialisation_pathway to auto-inform this dashboard.")
