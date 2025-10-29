# ============================================
# INNOVATION MENTOR APP
# PAGE: 05_IP_Management.py
# Function: Intellectual Property (IP) Assistant
# ============================================

import streamlit as st
import json
from pathlib import Path

# ----------------------------
# PAGE CONFIGURATION
# ----------------------------
st.set_page_config(page_title="IP Management", page_icon="💡")
st.title("💡 Intellectual Property (IP) Management Assistant")

st.markdown("""
This tool helps you identify which form of **Intellectual Property (IP)** protection best suits your innovation.
Answer the quick questions below, then view your recommended IP strategy.
---
""")

# ----------------------------
# LOAD QUESTIONS FROM JSON
# ----------------------------
data_path = Path("data/ip_questionnaire.json")

if not data_path.exists():
    st.error("❌ The file 'data/ip_questionnaire.json' was not found. Please make sure it exists.")
    st.stop()

with open(data_path, "r", encoding="utf-8") as f:
    ip_data = json.load(f)

questions = ip_data["questions"]

# ----------------------------
# INITIALIZE SCORES
# ----------------------------
ip_scores = {
    "Patent": 0,
    "Design": 0,
    "Trademark": 0,
    "Copyright": 0,
    "Trade Secret": 0
}

# ----------------------------
# QUESTIONNAIRE LOOP
# ----------------------------
st.subheader("🧭 Questionnaire")

for q in questions:
    st.markdown(f"**{q['question']}**")
    options = [opt["text"] for opt in q["options"]]
    answer = st.radio("", options, key=q["id"])
    st.write("")  # adds spacing

    # Update scores based on the selected answer
    for opt in q["options"]:
        if opt["text"] == answer:
            for ip_type in opt["adds"]:
                ip_scores[ip_type] += 1

    st.divider()

# ----------------------------
# GENERATE RESULTS
# ----------------------------
if st.button("🔍 Generate Recommendation"):
    sorted_scores = sorted(ip_scores.items(), key=lambda x: x[1], reverse=True)
    top_types = [t for t, s in sorted_scores if s >= 2]

    st.subheader("📊 Your IP Profile")

    if top_types:
        st.success(f"**Recommended Protection:** {', '.join(top_types)}")

        st.markdown("""
        Phase 2 will include detailed rationale, CIPC/WIPO guidance, and next-step actions
        for each recommended IP type.
        """)

        st.markdown("You can later save your results to your Innovation Portfolio.")
    else:
        st.info("No strong recommendation yet — please review your answers.")
