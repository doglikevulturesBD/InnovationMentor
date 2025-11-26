# ============================================================
# INNOVATION MENTOR APP
# PAGE: 07_IP_Management.py
# COMPLETE & POLISHED EDITION
# ============================================================

import streamlit as st
import json
from pathlib import Path

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="IP Management", layout="wide")

st.title("🔐 Intellectual Property (IP) Management Assistant")
st.caption("A guided tool to help innovators determine the best IP protection strategy.")
st.markdown("""
This tool evaluates the nature of your innovation and recommends the most suitable form 
of intellectual property protection.  
Answer the short questionnaire below to receive your personalised IP pathway.

---
""")

# ----------------------------
# LOAD QUESTIONNAIRE JSON
# ----------------------------
q_path = Path("data/ip_questionnaire.json")
if not q_path.exists():
    st.error("❌ Missing file: `ip_questionnaire.json` in /data")
    st.stop()

try:
    with open(q_path, "r", encoding="utf-8") as f:
        questions = json.load(f)["questions"]
except Exception as e:
    st.error(f"❌ Error loading ip_questionnaire.json: {e}")
    st.stop()

# ----------------------------
# LOAD RATIONALE JSON
# ----------------------------
r_path = Path("data/ip_rationale.json")
if not r_path.exists():
    st.error("❌ Missing file: `ip_rationale.json` in /data")
    st.stop()

try:
    with open(r_path, "r", encoding="utf-8") as f:
        rationale_data = json.load(f)
except Exception as e:
    st.error(f"❌ Error loading ip_rationale.json: {e}")
    st.stop()


# ----------------------------
# RENDER QUESTIONNAIRE
# ----------------------------
st.header("📋 IP Questionnaire")

for q in questions:
    st.radio(
        q["question"],
        list(q["options"].keys()),
        key=q["id"]
    )


# ----------------------------
# SCORING ENGINE
# ----------------------------
ip_types = ["Patent", "Design", "Trademark", "Copyright", "Trade Secret"]
ip_scores = {ip: 0 for ip in ip_types}

for q in questions:
    user_choice = st.session_state.get(q["id"])
    if user_choice:
        weight_map = q["options"][user_choice]  # dict of ip → score
        for ip_type, score in weight_map.items():
            ip_scores[ip_type] += score

# Rank the IP types
sorted_scores = sorted(ip_scores.items(), key=lambda x: x[1], reverse=True)


# ----------------------------
# RESULTS DISPLAY
# ----------------------------
st.markdown("---")
if st.button("Show My IP Recommendation", use_container_width=True):

    primary_ip, primary_score = sorted_scores[0]
    secondary_ip, secondary_score = sorted_scores[1]

    # ----------------------------
    # MAIN RECOMMENDATIONS
    # ----------------------------
    st.success(f"🏆 Primary Recommendation: **{primary_ip}** (score {primary_score})")
    st.info(f"✨ Secondary Consideration: **{secondary_ip}** (score {secondary_score})")

    st.markdown("---")

    # ----------------------------
    # DETAILS FOR PRIMARY IP TYPE
    # ----------------------------
    ip_info = rationale_data.get(primary_ip, {})

    st.write("### 📘 Description")
    st.write(ip_info.get("description", "No description found."))

    st.write("### 🧭 Recommended Next Steps")
    for step in ip_info.get("next_steps", []):
        st.write(f"- {step}")

    st.write("### 💰 Approximate Cost")
    st.write(ip_info.get("approx_cost", "No cost information available."))

    st.markdown("---")

    # ----------------------------
    # RISK WARNINGS
    # ----------------------------
    st.write("### ⚠️ Key Risks & Limitations")

    risk_map = {
        "Patent": [
            "Public disclosure before filing destroys novelty.",
            "International filings become expensive very quickly.",
            "Maintenance fees are required to keep protection active."
        ],
        "Design": [
            "Protects only appearance, not function.",
            "Disclosure before filing destroys novelty."
        ],
        "Trademark": [
            "Generic or descriptive names cannot be registered.",
            "Conflicts with existing trademarks can block approval."
        ],
        "Copyright": [
            "Protects expression, not ideas or concepts.",
            "Code algorithms are not protected — only written form."
        ],
        "Trade Secret": [
            "Protection ends immediately if secrecy is lost.",
            "Difficult to enforce without strong internal processes."
        ]
    }

    for risk in risk_map.get(primary_ip, []):
        st.write(f"- {risk}")

    st.markdown("---")

    # ----------------------------
    # DISCLAIMER
    # ----------------------------
    st.info(
        "This tool provides early-stage guidance only. For formal legal advice, "
        "consult a registered IP attorney or IP specialist."
    )

