# ============================================
# INNOVATION MENTOR APP
# PAGE: 05_IP_Management.py
# MVP — Compatible with simple JSON structure
# ============================================

import streamlit as st
import json
from pathlib import Path

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="IP Management", layout="wide")
st.title("🔐 Intellectual Property (IP) Management Assistant")
st.caption("A guided tool to help you identify the most suitable IP protection pathway for your innovation.")

st.markdown("""
This assistant evaluates **what type of intellectual property protection** is best suited for your innovation.

Answer the questions below to receive a **recommended IP strategy** with detailed explanations.

---
""")

# ----------------------------
# LOAD QUESTIONS
# ----------------------------
q_path = Path("data/ip_questionnaire.json")
if not q_path.exists():
    st.error("❌ Missing: `ip_questionnaire.json`")
    st.stop()

with open(q_path, "r", encoding="utf-8") as f:
    questions = json.load(f)["questions"]

# ----------------------------
# LOAD RATIONALE
# ----------------------------
r_path = Path("data/ip_rationale.json")
if not r_path.exists():
    st.error("❌ Missing: `ip_rationale.json`")
    st.stop()

with open(r_path, "r", encoding="utf-8") as f:
    rationale = json.load(f)

# ----------------------------
# INITIALISE SCORES
# ----------------------------
ip_types = ["Patent", "Design", "Trademark", "Copyright", "Trade Secret"]
scores = {ip: 0 for ip in ip_types}

# ----------------------------
# RENDER QUESTIONNAIRE
# ----------------------------
st.subheader("🧩 Answer the following questions")

answers = {}

for q in questions:
    st.markdown(f"**{q['question']}**")

    option_labels = [opt["text"] for opt in q["options"]]

    selected_label = st.radio(
        label="",
        options=option_labels,
        key=f"q_{q['id']}",
        horizontal=False
    )

    # Save selected option object
    for opt in q["options"]:
        if opt["text"] == selected_label:
            answers[q["id"]] = opt
            break

# ----------------------------
# PROCESS RESULTS
# ----------------------------
if st.button("🔍 Analyse My IP Strategy"):
    # Tally up IP scores
    for qid, opt in answers.items():
        for ip in opt["adds"]:
            scores[ip] += 1

    # Ranking
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # ----------------------------
    # OUTPUT RESULTS
    # ----------------------------
    st.markdown("---")
    st.header("🏆 Recommended IP Protection")

    top_ip, top_score = ranked[0]

    st.markdown(f"""
    ### ⭐ **Primary Recommendation: {top_ip}**
    {rationale[top_ip]["summary"]}
    """)

    st.markdown("### 🥈 Other relevant options")
    for ip, score in ranked[1:3]:
        st.markdown(f"**{ip}** — {rationale[ip]['short']}")

    st.markdown("---")

    with st.expander("📘 Full IP Guide"):
        for ip in ip_types:
            st.markdown(f"""
            #### **{ip}**
            {rationale[ip]["details"]}
            """)

    # Debug scores (optional)
    # st.write(scores)
