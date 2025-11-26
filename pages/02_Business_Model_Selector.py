import json
import streamlit as st
import pandas as pd

from config.business_model_questions import QUESTION_DEFS
from utils.bm_rule_engine import load_weights, calculate_rule_scores
from utils.bm_ai_engine import ai_scores_for_models
from utils.bm_fusion import fuse_scores


st.set_page_config(
    page_title="Business Model Selector",
    page_icon="🧩",
    layout="wide"
)

st.title("Business Model Selector")
st.markdown(
    """
    This engine uses a structured 45-question diagnostic + an optional AI layer  
    to rank **70 business models** for your innovation.  
    """
)

# ---------------------------------------------------------------------
# 1. LOAD BUSINESS MODELS JSON
# ---------------------------------------------------------------------

with open("data/business_models.json", "r") as f:
    RAW_MODELS = json.load(f)

# Convert list → dict by ID
BM_DEFS = {m["id"]: m for m in RAW_MODELS}

MODEL_IDS = list(BM_DEFS.keys())


# ---------------------------------------------------------------------
# 2. RENDER QUESTIONNAIRE
# ---------------------------------------------------------------------
st.markdown("### Step 1: Answer the Business Model Questionnaire")

answers = {}
selected_features = []

for q in QUESTION_DEFS:

    # Conditional visibility rules
    if "visible_if" in q:
        cond = q["visible_if"]
        controlling_qid = list(cond.keys())[0]
        allowed_values = cond[controlling_qid]

        if controlling_qid not in answers:
            continue

        if answers[controlling_qid] not in allowed_values:
            continue

    labels = list(q["options"].keys())
    selected_label = st.selectbox(q["label"], labels, key=q["id"])

    feature_code = q["options"][selected_label]
    answers[q["id"]] = feature_code
    selected_features.append(feature_code)

st.markdown("---")


# ---------------------------------------------------------------------
# 3. OPTIONAL AI INPUT
# ---------------------------------------------------------------------
st.markdown("### Step 2: Optional AI Assistance")

extra_text = st.text_area(
    "Add any free-text description to help the AI refine recommendations.",
    placeholder="Describe your innovation, customer, problem, TRL, value, etc.",
    key="bm_ai_extra_text"
)

full_text = extra_text.strip()


# ---------------------------------------------------------------------
# 4. GENERATE RESULTS
# ---------------------------------------------------------------------
if st.button("Generate Business Model Recommendations"):

    if not selected_features:
        st.warning("Please complete the questionnaire first.")
        st.stop()

    # Load weight matrix
    weights = load_weights("data/bm_rule_weights.json")

    # RULE-ONLY SCORES
    rule_scores = calculate_rule_scores(selected_features, weights)

    # AI SCORES (zero if no embeddings configured)
    ai_scores = ai_scores_for_models(full_text, MODEL_IDS)

    # Combine rule-based + AI weights (default 70/30)
    final_scores = fuse_scores(rule_scores, ai_scores, rule_weight=0.7)

    # Sort models
    ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
    top3 = [m for m, _ in ranked[:3]]

    # Save to session state
    st.session_state["top3_models"] = top3
    st.session_state["business_model_scores"] = final_scores

    st.success("Top 3 business models identified!")
    st.markdown("## Top 3 Recommended Models")

    for model_id in top3:
        info = BM_DEFS.get(model_id, {})
        st.subheader(f"• {info.get('name', model_id)}")
        st.write(info.get("description", ""))

    # Full ranking table
    with st.expander("Show complete rankings"):
        rows = []
        for model_id, score in ranked:
            info = BM_DEFS.get(model_id, {})
            rows.append({
                "ID": model_id,
                "Name": info.get("name", model_id),
                "Hybrid Score": round(score, 4)
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)


# -----------------------------------------------
# 5. SHOW CURRENT RESULTS IF PAGE REFRESHES
# -----------------------------------------------
elif "top3_models" in st.session_state:
    st.markdown("## Current Top 3 Models")

    for model_id in st.session_state["top3_models"]:
        info = BM_DEFS.get(model_id, {})
        st.subheader(f"• {info.get('name', model_id)}")
        st.write(info.get("description", ""))




