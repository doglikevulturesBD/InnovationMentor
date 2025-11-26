FILE: app.py
import streamlit as st
from config.business_model_questions import QUESTION_DEFS
from engine.scorer import rank_business_models
import numpy as np

st.set_page_config(page_title="Business Model Selector", layout="wide")

st.title("Business Model Selector (AI + Rules Engine)")

selected_answers = {}
tag_vectors = []  # In MVP1 you can use dummy vectors or map tags → vectors later.


# ---------------------------
# Render questions
# ---------------------------
st.header("Answer the 45 questions")

for q in QUESTION_DEFS:
    qid = q["id"]
    label = q["label"]
    options = list(q["options"].keys())

    selected = st.radio(label, options, key=qid)
    selected_answers[qid] = q["options"][selected]

# ---------------------------
# Run scoring
# ---------------------------
if st.button("Compute Top Business Models"):
    top3, full = rank_business_models(selected_answers, tag_vectors)

    st.subheader("Top 3 Recommended Models")
    for bm, score in top3:
        st.write(f"**{bm}** — score {score:.4f}")

    st.markdown("---")

    st.subheader("Full ranking")
    for bm, score in full:
        st.write(f"{bm}: {score:.4f}")


This version already works even if the AI embeddings are empty — you can later plug in real embeddings.

🎯 WHAT YOU MUST COPY–PASTE (SUMMARY)
Copy these EXACTLY:
Folders
/config
/data
/engine

Files
config/scoring_config.json
config/ai_config.json
config/business_model_questions.py    ← your existing file

data/business_models.json
data/bm_rule_weights.json
data/bm_model_vectors.json

engine/rules_engine.py
engine/ai_engine.py
engine/scorer.py

app.py
