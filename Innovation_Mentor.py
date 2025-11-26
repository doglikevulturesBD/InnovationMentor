import streamlit as st
from config.business_model_questions import QUESTION_DEFS
from engine.scorer import rank_business_models
import numpy as np

st.set_page_config(page_title="Business Model Selector", layout="wide")

st.title("Business Model Selector (AI + Rules Engine)")

selected_answers = {}


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
    # AI disabled for now
    top3, full = rank_business_models(selected_answers, user_vector=None)

    st.subheader("Top 3 Recommended Models")
    for bm, score in top3:
        st.write(f"**{bm}** — score {score:.4f}")

    st.markdown("---")

    st.subheader("Full ranking")
    for bm, score in full:
        st.write(f"{bm}: {score:.4f}")


