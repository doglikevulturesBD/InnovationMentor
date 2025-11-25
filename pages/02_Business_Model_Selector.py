# ============================================
# INNOVATION MENTOR APP
# PAGE: 03_Business_Model.py
# ============================================

import streamlit as st
from utils.model_logic import (
    load_models,
    QUESTION_BANK,
    accumulate_tags,
    trl_gate_score_adjustments,
    score_models,
    apply_trl_caps,
    find_adjacent_models
)

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Business Model Recommender", layout="wide")
st.title("💼 Business Model Recommender")
st.markdown("""
Use this structured questionnaire to identify which business model patterns  
best align with your innovation, TRL level, revenue logic, and delivery strategy.
---
""")


# =============================
# Load models & initialise state
# =============================
models = load_models()

if "bm_answers" not in st.session_state:
    st.session_state["bm_answers"] = {}

if "trl_level" not in st.session_state:
    st.session_state["trl_level"] = None


# =============================
# TRL INPUT (optional but powerful)
# =============================
st.subheader("💡 Technology Readiness Level (Optional)")
trl = st.slider("Select TRL (1–9)", min_value=1, max_value=9, value=5)
st.session_state["trl_level"] = trl

st.markdown("---")


# =============================
# QUESTIONNAIRE
# =============================
st.subheader("📋 Business Model Questionnaire")

for q in QUESTION_BANK:
    with st.container():
        st.markdown(f"**{q['id']} – {q['section']}**")
        answer = st.radio(
            q["text"],
            list(q["options"].keys()),
            key=f"bm_{q['id']}"
        )
        st.session_state["bm_answers"][q["id"]] = answer

st.markdown("---")


# =============================
# RUN ENGINE
# =============================
if st.button("🔍 Generate Business Model Recommendations"):
    st.subheader("📊 Your Business Model Profile")

    selections = {qid: ans for qid, ans in st.session_state["bm_answers"].items()}

    # Step 1 – accumulate raw tag weights
    tag_weights = accumulate_tags(selections)

    # Step 2 – adjust for TRL
    tag_weights = trl_gate_score_adjustments(tag_weights, trl)

    # Step 3 – score
    scored = score_models(tag_weights, models, top_k=3)

    # Step 4 – apply TRL caps
    scored = apply_trl_caps(scored, trl)

    # ========================================
    # DISPLAY TOP MODELS
    # ========================================
    for idx, item in enumerate(scored, start=1):
        m = item["model"]
        score = item["score"]
        matched = item["matched"]
        penalties = item["penalties"]

        st.markdown(f"### {idx}. **{m['name']}**")
        st.markdown(f"**Cluster:** {m.get('cluster', 'General')}")
        st.markdown(f"**Score:** `{score}`")
        st.markdown(f"**Tags:** `{', '.join(m.get('tags', []))}`")

        # Description
        with st.expander("📘 Model Description"):
            st.markdown(m["description"])

        # Matched tags
        with st.expander("🔑 Why this model matched your inputs"):
            if matched:
                for t, w in matched.items():
                    st.markdown(f"- `{t}` (weight {w})")
            else:
                st.markdown("_No key overlaps – recommended due to TRL logic or fallback scoring._")

        # Penalties
        if penalties:
            with st.expander("⚠️ Penalties / Risk Misalignment"):
                for t, w in penalties.items():
                    st.markdown(f"- `{t}` → penalty `{w}`")

        # Similarity graph
        sim = find_adjacent_models(m, models)
        if sim:
            with st.expander("🔁 Related / Similar Models"):
                for s in sim:
                    st.markdown(
                        f"- **{s['model']['name']}** "
                        f"(similarity `{s['similarity']}`)"
                    )

        st.markdown("---")


    # ========================================
    # DISPLAY RAW TAG WEIGHT PROFILE
    # ========================================
    with st.expander("🧠 Your underlying tag preference profile"):
        st.json(dict(tag_weights))


# =============================
# REFLECTION BOX
# =============================
st.markdown("## 📝 Reflection")
st.markdown("""
Use this space to note insights, adjustments, or ideas that came from your Business Model analysis.
""")
st.text_area("Your reflections:", height=150)


