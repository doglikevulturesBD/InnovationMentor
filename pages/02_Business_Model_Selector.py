# pages/02_Business_Model_Selector.py
import streamlit as st
from collections import Counter
from utils.model_logic import (
    QUESTION_BANK, load_models, accumulate_tags,
    trl_gate_score_adjustments, score_models
)
from utils.reflection_manager import enforce_reflection


# -------- Session State --------
if "bm_step" not in st.session_state: st.session_state.bm_step = 0
if "bm_answers" not in st.session_state: st.session_state.bm_answers = {}
if "bm_done" not in st.session_state: st.session_state.bm_done = False


# -------- Navigation Logic --------
def go_next(choice: str):
    q = QUESTION_BANK[st.session_state.bm_step]
    st.session_state.bm_answers[q["id"]] = choice
    st.session_state.bm_step += 1
    if st.session_state.bm_step >= len(QUESTION_BANK):
        st.session_state.bm_done = True

def go_back():
    if st.session_state.bm_step == 0: 
        return
    st.session_state.bm_step -= 1
    q = QUESTION_BANK[st.session_state.bm_step]
    st.session_state.bm_answers.pop(q["id"], None)

def restart():
    st.session_state.bm_step = 0
    st.session_state.bm_answers = {}
    st.session_state.bm_done = False


# -------- Header --------
st.title("🧩 Business Model Selector — Profiler")
st.caption("This wizard evaluates your innovation across 40 signals to recommend your best-fit business models.")

# Show TRL if captured previously
trl = st.session_state.get("trl_level", None)
if trl is not None:
    st.info(f"Detected from TRL page: **TRL {trl}**")

st.markdown("---")

# -------- Progress --------
progress = st.session_state.bm_step / len(QUESTION_BANK)
st.progress(progress)


# ========== Wizard Flow ==========
if not st.session_state.bm_done and st.session_state.bm_step < len(QUESTION_BANK):

    q = QUESTION_BANK[st.session_state.bm_step]

    st.markdown(f"### {q['section']} — Question {st.session_state.bm_step + 1} of {len(QUESTION_BANK)}")
    st.markdown(f"**{q['text']}**")

    # Restore previous selection if using Back
    prev = st.session_state.bm_answers.get(q["id"], None)
    options = list(q["options"].keys())
    default_index = options.index(prev) if prev in options else 0

    choice = st.radio(
        "",
        options,
        index=default_index,
        key=f"bm_q_{q['id']}",
        label_visibility="collapsed"
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("⬅ Back", on_click=go_back, disabled=(st.session_state.bm_step == 0))
    with col2:
        st.button("Next ➜", on_click=lambda: go_next(choice), type="primary")

# ========== Results ==========
else:
    base_weights: Counter = accumulate_tags(st.session_state.bm_answers)
    adjusted_weights = trl_gate_score_adjustments(base_weights, trl)

    models = load_models()
    top3 = score_models(adjusted_weights, models, top_k=3)

    st.success(f"### 🎯 Questionnaire Complete!")
    st.write(f"You generated **{sum(abs(v) for v in adjusted_weights.values())} weighted signals**.")

    st.markdown("### 🏆 Top Recommended Business Models")

    names_for_next = []
    for i, item in enumerate(top3, start=1):
        m = item["model"]
        names_for_next.append(m["name"])
        
        st.markdown(f"**{i}. {m['name']}** — Score: `{item['score']}`")
        st.caption(m.get("description", ""))

        with st.expander("Matched Tags"):
            st.write(item["matched"] or "No strong positive tag matches.")

        if item["penalties"]:
            with st.expander("Penalties / Fit Issues"):
                st.write(item["penalties"])

    st.divider()

    # EXPORT TO NEXT MODULE
    st.markdown("### 📤 Export to Next Steps")
    if names_for_next:
        selected = st.selectbox("Choose a model for financial projection:", names_for_next)
        st.session_state["selected_model"] = selected
        st.success(f"Saved: **{selected}** → You can now proceed to Financial Projections.")

    col1, col2 = st.columns([1, 1])
    col1.button("🔁 Restart", on_click=restart)
    col2.page_link("pages/03_Financial_Projection.py", label="➡ Go to Financial Projection", icon="💰")

    st.divider()

    # ------- Reflection -------
    st.markdown("### 💬 Reflection")
    enforce_reflection("business_model")



