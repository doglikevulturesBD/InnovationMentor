# ============================================
# INNOVATION MENTOR APP
# PAGE: 05_IP_Management.py
# MVP — Polished Edition (Working Version)
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
This assistant evaluates **what type of intellectual property protection** is best suited for your innovation based on its 
characteristics, novelty, branding needs, and confidentiality aspects.

Answer the questions below to receive a **recommended IP protection strategy** along with explanations and next steps.

---
""")

# ----------------------------
# LOAD QUESTIONS
# ----------------------------
q_path = Path("data/ip_questionnaire.json")
if not q_path.exists():
    st.error("❌ Missing file: `ip_questionnaire.json` in /data")
    st.stop()

with open(q_path, "r", encoding="utf-8") as f:
    questions = json.load(f)["questions"]

# ----------------------------
# LOAD RATIONALE
# ----------------------------
r_path = Path("data/ip_rationale.json")
if not r_path.exists():
    st.error("❌ Missing file: `ip_rationale.json` in /data")
    st.stop()

with open(r_path, "r", encoding="utf-8") as f:
    rationale_data = json.load(f)

# ----------------------------
# INITIALISE SCORES
# ----------------------------
ip_types = ["Patent", "Design", "Trademark", "Copyright", "Trade Secret"]
ip_scores = {ip: 0 for ip in ip_types}


# ----------------------------
# RENDER QUESTIONNAIRE
# ----------------------------
st.subheader("🧩 Answer the following questions")

responses = {}

for q in questions:
    qid = q["id"]
    text = q["question"]
    options = q["options"]

    st.markdown(f"**{text}**")

    selected = st.radio(
        label="",
        options=list(options.keys()),
        key=qid,
        horizontal=False
    )

    responses[qid] = selected


# ----------------------------
# PROCESS RESULTS
# ----------------------------
if st.button("🔍 Analyse My IP Profile"):
    st.markdown("---")

    # Score calculation
    for q in questions:
        qid = q["id"]
        selected = responses[qid]
        effects = q["options"][selected]

        # Add weights to each IP type
        for ip_type, weight in effects.items():
            ip_scores[ip_type] += weight

    # Sort by score
    ranked = sorted(ip_scores.items(), key=lambda x: x[1], reverse=True)

    # ----------------------------
    # DISPLAY TOP RECOMMENDATIONS
    # ----------------------------
    st.header("🏆 Your Recommended IP Protection Strategy")

    top_ip, top_score = ranked[0]

    st.markdown(f"""
    ### ⭐ **Primary Recommendation: {top_ip}**
    {rationale_data[top_ip]["summary"]}
    """)

    # Optional: show top 3
    st.markdown("### 🥈 Other strong matches")
    for ip, score in ranked[1:3]:
        st.markdown(f"- **{ip}** — {rationale_data[ip]['short']}")

    st.markdown("---")

    # ----------------------------
    # DISPLAY FULL BREAKDOWN
    # ----------------------------
    with st.expander("📘 Full Explanations of All IP Types", expanded=False):
        for ip in ip_types:
            st.markdown(f"""
            #### **{ip}**
            {rationale_data[ip]["details"]}
            """)

    # ----------------------------
    # RAW SCORE DEBUG (optional)
    # ----------------------------
    # st.write("Raw scores:", ip_scores)
