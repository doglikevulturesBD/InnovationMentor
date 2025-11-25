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
    "This engine uses a structured 45-question diagnostic + an optional AI layer "
    "to rank 70 business models for your innovation."
)

# ---------------------------------------------------------------------
# 1. LOAD BUSINESS MODEL DEFINITIONS (your JSON list → dict conversion)
# ---------------------------------------------------------------------
with open("data/business_models.json", "r") as f:
    BM_RAW = json.load(f)

# AUTO-CONVERT LIST → DICT USING "id"
if isinstance(BM_RAW, list):
    BM_DEFS = {item["id"]: item for item in BM_RAW}
else:
    BM_DEFS = BM_RAW

MODEL_NAMES = list(BM_DEFS.keys())
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# 2. RENDER QUESTIONNAIRE WITH CONDITIONAL LOGIC
# ---------------------------------------------------------------------
st.markdown("### Step 1: Questionnaire")

answers = {}
selected_features = []

for q in QUESTION_DEFS:

    # Conditional visibility logic
    if "visible_if" in q:
        condition = q["visible_if"]
        controlling_qid = list(condition.keys())[0]
        allowed_values = condition[controlling_qid]

        # skip if controller unanswered
        if controlling_qid not in answers:
            continue

        # skip if controller not in allowed values
        if answers[controlling_qid] not in allowed_values:
            continue

    labels = list(q["options"].keys())
    selected_label = st.selectbox(
        q["label"],
        labels,
        key=q["id"]
    )

    selected_feature = q["options"][selected_label]
    answers[q["id"]] = selected_feature
    selected_features.append(selected_feature)

st.markdown("---")


# ---------------------------------------------------------------------
# 3. AI INPUT
# ---------------------------------------------------------------------
st.markdown("### Step 2: Describe your innovation (for AI layer)")

summary_parts = [
    st.session_state.get("project_summary", ""),
    st.session_state.get("value_proposition", ""),
    st.session_state.get("customer_segment_text", ""),
    st.session_state.get("trl_description", ""),
]

extra_text = st.text_area(
    "Optional free-text description to help the AI refine recommendations:",
    key="bm_ai_extra_text"
)

full_text = "\n".join([p for p in summary_parts if p] + [extra_text])


# ---------------------------------------------------------------------
# 4. GENERATE SCORES
# ---------------------------------------------------------------------
if st.button("Generate Business Model Recommendations"):

    if not selected_features:
        st.warning("Please answer the questionnaire first.")
        st.stop()

    # Load weight matrix
    weights = load_weights("config/business_model_weights.json")

    # RULE-BASED SCORES
    rule_scores = calculate_rule_scores(selected_features, weights)

    # AI SCORES (0 if no embeddings yet)
    ai_scores = ai_scores_for_models(full_text, MODEL_NAMES)

    # HYBRID 70/30
    final_scores = fuse_scores(rule_scores, ai_scores, rule_weight=0.7)

    # SORT
    ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
    top3 = [m for m, _ in ranked[:3]]

    # Save to state
    st.session_state["top3_models"] = top3
    st.session_state["business_model_scores"] = final_scores

    st.success("Top 3 business models identified.")

    # -----------------------------------------------------------------
    # 5. DISPLAY TOP 3 RESULTS
    # -----------------------------------------------------------------
    st.markdown("## Top 3 Recommended Business Models")

    for model_id in top3:
        info = BM_DEFS.get(model_id, {})
        st.subheader(f"• {info.get('name', model_id)}")
        st.write(info.get("description", ""))

    # Full ranking table
    with st.expander("Show all business model scores"):
        rows = []
        for model_id, score in ranked:
            info = BM_DEFS.get(model_id, {})
            rows.append({
                "ID": model_id,
                "Name": info.get("name", model_id),
                "Hybrid Score": round(score, 2)
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)


# ---------------------------------------------------------------------
# 6. DISPLAY LAST RESULTS IF PAGE IS RELOADED
# ---------------------------------------------------------------------
elif "top3_models" in st.session_state:
    st.markdown("## Current Top 3 Business Models")

    for model_id in st.session_state["top3_models"]:
        info = BM_DEFS.get(model_id, {})
        st.subheader(f"• {info.get('name', model_id)}")
        st.write(info.get("description", ""))



