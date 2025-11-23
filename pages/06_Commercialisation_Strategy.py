# ============================================
# INNOVATION MENTOR APP
# PAGE: 06_Commercialisation_Strategy.py
# FUNCTION: Combined Commercialisation & Marketing Strategy Advisor
# ============================================

import streamlit as st
import json
from pathlib import Path
from collections import defaultdict

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Commercialisation & Marketing Strategy", page_icon="🚀")
st.title("Commercialisation & Marketing Strategy Advisor")

st.markdown("""
This tool helps you identify **how to take your innovation to market** — by recommending the most suitable **commercialisation pathway** 
(e.g., Licensing, Direct Sales, Partnerships) and the top **marketing strategies** to build awareness and adoption.

Answer the following questions to receive your tailored strategy mix.
---
""")

# ----------------------------
# LOAD QUESTIONNAIRE
# ----------------------------
data_path = Path("data/commercialisation_questionnaire.json")

if not data_path.exists():
    st.error("❌ The file 'commercialisation_questionnaire.json' was not found. Please ensure it exists in the /data folder.")
    st.stop()

with open(data_path, "r", encoding="utf-8") as f:
    questions = json.load(f)["questions"]

# ----------------------------
# INITIALIZE SCORES
# ----------------------------
commercialisation_scores = defaultdict(int)
marketing_scores = defaultdict(int)

# ----------------------------
# QUESTIONNAIRE LOOP
# ----------------------------
st.subheader("🧭 Questionnaire")

for q in questions:
    st.markdown(f"**{q['question']}**")
    options = [opt["text"] for opt in q["options"]]
    answer = st.radio("", options, key=f"q{q['id']}")
    st.write("")  # spacing
    
    for opt in q["options"]:
        if opt["text"] == answer:
            for c_item in opt["adds"]["commercialisation"]:
                commercialisation_scores[c_item] += 1
            for m_item in opt["adds"]["marketing"]:
                marketing_scores[m_item] += 1
    st.divider()

# ----------------------------
# GENERATE RECOMMENDATIONS
# ----------------------------
if st.button("🔍 Generate My Strategy Mix"):
    st.subheader("📊 Your Commercialisation & Marketing Strategy Mix")

    # --- Sort and get top results
    sorted_commercialisation = sorted(commercialisation_scores.items(), key=lambda x: x[1], reverse=True)
    sorted_marketing = sorted(marketing_scores.items(), key=lambda x: x[1], reverse=True)

    top_commercialisation = sorted_commercialisation[0][0] if sorted_commercialisation else None
    top3_marketing = [t for t, s in sorted_marketing[:3]]

    if not top_commercialisation:
        st.info("No clear commercialisation pathway identified yet — please review your answers.")
        st.stop()

    # --- Display Results
    st.success(f"**Recommended Commercialisation Pathway:** {top_commercialisation}")
    st.info(f"**Top 3 Marketing Strategies:** {', '.join(top3_marketing)}")

    st.markdown("---")
    st.subheader("🧩 Strategy Breakdown")

    # --- Load rationale JSON (Phase 2 placeholder)
    rationale_path = Path("data/commercialisation_rationale.json")
    if rationale_path.exists():
        with open(rationale_path, "r", encoding="utf-8") as f:
            rationale_data = json.load(f)
    else:
        rationale_data = {}

    # --- Display detailed rationales
    if top_commercialisation in rationale_data:
        data = rationale_data[top_commercialisation]
        with st.expander(f"🚀 {top_commercialisation} – Details & Next Steps"):
            st.markdown(f"**Description:** {data['description']}")
            st.markdown("**Next Steps:**")
            for step in data["next_steps"]:
                st.markdown(f"- {step}")
            st.markdown(f"**Estimated Cost / Complexity:** {data['cost']}")
            st.markdown("---")

    for m in top3_marketing:
        if m in rationale_data:
            data = rationale_data[m]
            with st.expander(f"🎯 {m} – Marketing Approach"):
                st.markdown(f"**Description:** {data['description']}")
                st.markdown("**Tactics:**")
                for t in data["tactics"]:
                    st.markdown(f"- {t}")
                st.markdown(f"**Innovation Angle:** {data['innovation']}")
                st.markdown("---")

    st.caption("Phase 2 will include an exportable Go-to-Market PDF with timelines and KPI guidance.")
