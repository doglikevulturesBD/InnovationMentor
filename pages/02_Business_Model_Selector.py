# pages/02_Business_Model.py

import json
import streamlit as st

from config.business_model_questions import QUESTION_DEFS
from utils.bm_rule_engine import load_weights, calculate_rule_scores
from utils.bm_ai_engine import ai_scores_for_models
from utils.bm_fusion import fuse_scores


st.set_page_config(page_title="Business Model Selector", page_icon="🧩", layout="wide")

st.title("Business Model Selector")
st.markdown(
    "Answer the questions below to generate a ranked list of business models "
    "that fit your innovation. The engine uses both a structured ruleset and, "
    "optionally, an AI pattern-matching layer."
)

# --- Load business model definitions ---

with open("data/business_models.json", "r") as f:
    BM_DEFS = json.load(f)

MODEL_NAMES = list(BM_DEFS.keys())


# --- Questionnaire with conditional visibility ---

st.markdown("### Step 1: Tell us about your model")

answers = {}
selected_features = []

for q in QUESTION_DEFS:
    # Conditional visibility
    if "visible_if" in q:
        cond = q["visible_if"]
        controlling_qid = list(cond.keys())[0]
        allowed_feature_values = cond[controlling_qid]

        # If controlling question not yet answered, skip
        if controlling_qid not in answers:
            continue

        # If current controlling answer feature not allowed, skip
        if answers[controlling_qid] not in allowed_feature_values:
            continue

    options_labels = list(q["options"].keys())
    default_idx = 0

    # Use q["id"] as Streamlit key to persist answers
    chosen_label = st.selectbox(
        q["label"],
        options_labels,
        key=q["id"],
        index=default_idx,
    )
    feature_key = q["options"][chosen_label]
    answers[q["id"]] = feature_key
    selected_features.append(feature_key)

st.markdown("---")

# --- AI input text ---

st.markdown("### Step 2: Describe your innovation (for AI layer)")

summary_parts = [
    st.session_state.get("project_summary", ""),
    st.session_state.get("value_proposition", ""),
    st.session_state.get("customer_segment_text", ""),
    st.session_state.get("trl_description", ""),
]

extra_text = st.text_area(
    "Optional: add any extra context in your own words (this helps the AI refine suggestions)",
    key="bm_ai_extra_text",
)

full_text = "\n".join([p for p in summary_parts if p] + [extra_text])


# --- Action button ---

if st.button("Generate Business Model Recommendations"):
    if not selected_features:
        st.warning("Please answer at least some of the questions first.")
    else:
        # Load weights
        weights = load_weights("config/business_model_weights.json")

        # Rule-based scores
        rule_scores = calculate_rule_scores(selected_features, weights)

        # AI scores (0 if not configured yet)
        ai_scores = ai_scores_for_models(full_text, MODEL_NAMES)

        # Hybrid fusion
        final_scores = fuse_scores(rule_scores, ai_scores, rule_weight=0.7)

        # Sort and select top 3
        ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        top3 = [m for m, _ in ranked[:3]]

        st.session_state["top3_models"] = top3
        st.session_state["business_model_scores"] = final_scores

        st.success("Top 3 business models identified.")

        st.markdown("### Your Top 3 Business Models")

        for model in top3:
            info = BM_DEFS.get(model, {})
            name = info.get("name", model)
            desc = info.get("description", "")
            st.subheader(f"• {name}")
            if desc:
                st.write(desc)

        # Optional: show a table with scores
        with st.expander("Show full model ranking (all models)"):
            import pandas as pd

            rows = []
            for m, score in ranked:
                info = BM_DEFS.get(m, {})
                rows.append(
                    {
                        "Model ID": m,
                        "Name": info.get("name", m),
                        "Score (hybrid)": round(score, 2),
                    }
                )
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True)
else:
    # If results already in session, show them
    if "top3_models" in st.session_state:
        st.markdown("### Current Top 3 Business Models")
        for model in st.session_state["top3_models"]:
            info = BM_DEFS.get(model, {})
            name = info.get("name", model)
            desc = info.get("description", "")
            st.subheader(f"• {name}")
            if desc:
                st.write(desc)


