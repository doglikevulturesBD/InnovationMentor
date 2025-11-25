# ============================================
# INNOVATION MENTOR APP
# PAGE: 07_Risk_Dashboard.py (MVP Polished Edition)
# FUNCTION: Hybrid Dynamic Risk Dashboard
# ============================================

import json
from pathlib import Path
from collections import defaultdict
import pandas as pd
import streamlit as st

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------
st.set_page_config(page_title="Risk Dashboard", layout="wide")
st.title("⚠️ Innovation Risk Dashboard")
st.caption("Identify, quantify, and mitigate the major risks limiting your innovation’s readiness.")

st.markdown("""
This dashboard blends a short **diagnostic questionnaire** with automatic context from other modules  
(TRL, Business Model, Marketing, Financing, Commercialisation, IP)  
to generate a tailored **Top Risk Profile** with practical mitigation steps.

---
""")

# ----------------------------------------------------
# Load JSON Assets
# ----------------------------------------------------
def load_json(path: str):
    p = Path(path)
    if not p.exists():
        st.error(f"❌ Missing file: `{path}`")
        st.stop()
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

engine = load_json("data/risk_engine.json")
library = load_json("data/risk_library.json")

weighting_rules = engine.get("weighting_rules", [])
questions = engine.get("questionnaire", [])
base_points = engine.get("scoring", {}).get("base_points_per_hit", 10)
top_n = engine.get("scoring", {}).get("top_n", 5)

# ----------------------------------------------------
# Read context (from other modules)
# ----------------------------------------------------
trl      = st.session_state.get("trl_level", 6)
bm       = st.session_state.get("selected_business_model", None)
funding  = st.session_state.get("funding_stage", "Seed")
mkt_str  = st.session_state.get("marketing_top_strategies", [])
comm     = st.session_state.get("commercialisation_pathway", None)

# ----------------------------------------------------
# Context Expander
# ----------------------------------------------------
with st.expander("ℹ️ Detected project context (editable)"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("TRL", 1, 9, int(trl), key="ctx_trl")
        st.selectbox("Funding stage", ["Pre-seed","Seed","Series A","Series B","Revenue"], index=1, key="ctx_funding")
    with col2:
        st.selectbox("Business model", ["Licensing","Direct Sales","Subscription","Franchising / Replication Model","Marketplace","Other"], key="ctx_bm")
        st.selectbox("Commercialisation pathway", ["Public-Private Pilot","Direct Sales","Licensing","Partnership / JV","Franchising","Digital Platform","Co-Development","Unknown"], key="ctx_comm")
    with col3:
        st.multiselect(
            "Top marketing strategies",
            ["Product Differentiation", "Cost / Value Leadership", "Niche / Community Focus",
             "Partnership & Co-Creation","Digital-First","Engagement / Experience",
             "Impact Branding","Community Growth","Ecosystem Storytelling"],
            default=mkt_str,
            key="ctx_mkt"
        )

# ----------------------------------------------------
# Questionnaire
# ----------------------------------------------------
st.subheader("📝 Quick Risk Questionnaire")

base_scores = defaultdict(int)
answers = {}
total_q = len(questions)

for i, q in enumerate(questions, start=1):
    st.markdown(f"### Question {i} of {total_q}")
    st.write(f"**{q['question']}**")

    opts = [o["text"] for o in q["options"]]
    choice = st.radio("", opts, key=f"risk_q_{q['id']}")

    answers[q["id"]] = choice

    selected_option = next(o for o in q["options"] if o["text"] == choice)
    for risk_type in selected_option.get("adds", []):
        base_scores[risk_type] += base_points

    st.progress(i / total_q)
    st.divider()

# ----------------------------------------------------
# Apply Contextual Weighting Rules
# ----------------------------------------------------
ctx = {
    "trl": int(st.session_state["ctx_trl"]),
    "business_model": st.session_state["ctx_bm"],
    "funding_stage": st.session_state["ctx_funding"],
    "marketing": set(st.session_state["ctx_mkt"]),
    "commercialisation": st.session_state["ctx_comm"]
}

weighted_scores = defaultdict(int, base_scores)
rule_hits = defaultdict(list)  # For tracing what rules contributed

def rule_matches(rule_when: dict) -> bool:
    if "trl_max" in rule_when and ctx["trl"] > rule_when["trl_max"]:
        return False
    if "business_model_any" in rule_when and ctx["business_model"] not in rule_when["business_model_any"]:
        return False
    if "funding_stage_any" in rule_when and ctx["funding_stage"] not in rule_when["funding_stage_any"]:
        return False
    if "marketing_any" in rule_when and not (ctx["marketing"] & set(rule_when["marketing_any"])):
        return False
    if "commercialisation_any" in rule_when and ctx["commercialisation"] not in rule_when["commercialisation_any"]:
        return False
    return True

for rule in weighting_rules:
    if rule_matches(rule.get("when", {})):
        for risk_type, bonus in rule.get("weights", {}).items():
            weighted_scores[risk_type] += bonus
            rule_hits[risk_type].append(rule.get("name", "context_rule"))

# ----------------------------------------------------
# Top Risks
# ----------------------------------------------------
sorted_risks = sorted(weighted_scores.items(), key=lambda x: x[1], reverse=True)
top_risks = [(r, s) for r, s in sorted_risks if s > 0][:top_n]

st.subheader("🔥 Top Risks")

if not top_risks:
    st.info("No major risks detected yet — adjust questionnaire or context.")
else:
    # Chart
    chart_df = pd.DataFrame(top_risks, columns=["Risk", "Score"]).set_index("Risk")
    st.bar_chart(chart_df)

    st.markdown("---")

    # Detailed breakdown
    for risk_type, score in top_risks:
        entry = library.get(risk_type, {})

        with st.expander(f"{risk_type} — Score {score}"):
            st.markdown(f"**Category:** {entry.get('category', '—')}")
            st.markdown(f"**Description:** {entry.get('description', '—')}")

            if entry.get("indicators"):
                st.markdown("**Indicators:**")
                for i in entry["indicators"]:
                    st.markdown(f"- {i}")

            if entry.get("mitigation"):
                st.markdown("**Mitigation:**")
                for m in entry["mitigation"]:
                    st.markdown(f"- {m}")

            st.markdown(f"**Severity (baseline):** {entry.get('severity', '—')}")

            if rule_hits.get(risk_type):
                with st.expander("Why this risk scored high?"):
                    for h in rule_hits[risk_type]:
                        st.markdown(f"- **{h}**")

# ----------------------------------------------------
# Download Risk Register
# ----------------------------------------------------
if top_risks:
    rows = []
    for r, score in top_risks:
        e = library.get(r, {})
        rows.append({
            "Risk": r,
            "Score": score,
            "Category": e.get("category", ""),
            "Severity": e.get("severity", ""),
            "Description": e.get("description", ""),
            "Mitigation 1": (e.get("mitigation", [""]))[0],
            "Mitigation 2": (e.get("mitigation", ["",""]))[1] if len(e.get("mitigation", [])) > 1 else "",
            "Mitigation 3": (e.get("mitigation", ["","",""]))[2] if len(e.get("mitigation", [])) > 2 else ""
        })

    df = pd.DataFrame(rows)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Risk Register (CSV)", csv, file_name="risk_register.csv", mime="text/csv")

st.caption("This dashboard adapts based on inputs from other modules. Complete TRL, Business Model, Market, Financial, and Strategy pages for richer insights.")


st.caption("Tip: Other pages can set session_state keys like trl_level, selected_business_model, funding_stage, marketing_top_strategies, commercialisation_pathway to auto-inform this dashboard.")
