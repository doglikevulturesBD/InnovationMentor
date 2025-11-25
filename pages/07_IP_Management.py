# ============================================
# INNOVATION MENTOR APP
# PAGE: 05_IP_Management.py
# MVP — Polished Edition
# ============================================

import streamlit as st
import json
from pathlib import Path

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="IP Management", layout="wide")
st.title("🔐 Intellectual Property (IP) Management Assistant")
st.caption("Determine the most suitable IP protection strategy for your innovation.")

st.markdown("""
This assistant helps you decide **what type of IP protection** best matches your innovation’s characteristics.  
Answer the short questionnaire below to receive your **recommended IP pathway** with descriptions and next steps.

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
# QUESTIONNAIRE
# ----------------------------
st.sub

