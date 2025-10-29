# ============================================
# INNOVATION MENTOR APP
# PAGE: 05_IP_Management.py
# PHASE 2 – adds rationale + next-steps
# ============================================

import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="IP Management", page_icon="💡")
st.title("💡 Intellectual Property (IP) Management Assistant")

st.markdown("""
This tool helps you identify which form of **Intellectual Property (IP)** protection best suits your innovation.
Answer the quick questions below, then view your recommended IP strategy.
---
""")

# ---------- Load Questions ----------
q_path = Path("data/ip_questionnaire.json")
if not q_path.exists():
    st.error("❌ 'ip_questionnaire.json' not found.")
    st.stop()
with open(q_path, "r", encoding="utf-8") as f:
    questions = json.load(f)["questions"]

# ---------- Load Rationale ----------
r_path = Path("data/ip_rationale.json")
if not r_path.exists():
    st.error("❌ 'ip_rationale.json' not found.")
    st.stop()
with open(r_path, "r", encoding="utf-8") as f:
    rationale_data = json.load(f)

# ---------- Initialise Scores ----------
ip_scores = {k: 0 for k in ["Patent", "Design", "Trademark", "Copyright", "Trade Secret"]}

# ---------- Questionnaire ----------
st.subheader("🧭 Questionnaire")

for q in questions:
    st.markdown(f"**{q['question']}**")
    options = [opt["text"] for opt in q["options"]]
    answer = st.radio("", options, key=q["id"])
    for opt in q["options"]:
        if opt["text"] == answer:
            for ip_type in opt["adds"]:
                ip_scores[ip_type] += 1
    st.divider()

# ---------- Results ----------
if st.button("🔍 Generate Recommendation"):
    st.subheader("📊 Your IP Profile")

    sorted_scores = sorted(ip_scores.items(), key=lambda x: x[1], reverse=True)
    top_types = [t for t, s in sorted_scores if s >= 2]

    if not top_types:
        st.info("No strong recommendation yet — please review your answers.")
        st.stop()

    st.success(f"**Recommended Protection:** {', '.join(top_types)}")
    st.markdown("---")

    # --- Display rationale for each recommended type ---
    for ip_type in top_types:
        data = rationale_data[ip_type]
        with st.expander(f"🔹 {ip_type} – click for details"):
            st.markdown(f"**Description:** {data['description']}")
            st.markdown("**Next Steps:**")
            for step in data["next_steps"]:
                st.markdown(f"- {step}")
            st.markdown(f"**Estimated Cost:** {data['approx_cost']}")
