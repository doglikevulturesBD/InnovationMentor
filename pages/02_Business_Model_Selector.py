# pages/02_Business_Model_Selector.py
import streamlit as st
from collections import Counter
from utils.model_logic import (
    QUESTION_BANK, load_models, accumulate_tags,
    trl_gate_score_adjustments, score_models
)


# -------- Session State --------
if "bm_step" not in st.session_state: st.session_state.bm_step = 0
if "bm_answers" not in st.session_state: st.session_state.bm_answers = {}   # {qid: option_label}
if "bm_done" not in st.session_state: st.session_state.bm_done = False

def go_next(choice: str):
    q = QUESTION_BANK[st.session_state.bm_step]
    st.session_state.bm_answers[q["id"]] = choice
    st.session_state.bm_step += 1
    if st.session_state.bm_step >= len(QUESTION_BANK):
        st.session_state.bm_done = True

def go_back():
    if st.session_state.bm_step == 0: return
    st.session_state.bm_step -= 1
    q = QUESTION_BANK[st.session_state.bm_step]
    st.session_state.bm_answers.pop(q["id"], None)

def restart():
    st.session_state.bm_step = 0
    st.session_state.bm_answers = {}
    st.session_state.bm_done = False

# -------- Header --------
st.title("Business Model Selector — Profiler")
st.caption("Answer a 40-question wizard. We’ll compute weighted tags and recommend your top business models.")

# Optional: show TRL level if present
trl = st.session_state.get("trl_level", None)
if trl is not None:
    st.info(f"Detected TRL from your TRL Calculator: **TRL {trl}**")

# -------- Progress --------
progress = st.session_state.bm_step / len(QUESTION_BANK)
st.progress(progress)

# -------- Wizard Flow --------
if not st.session_state.bm_done and st.session_state.bm_step < len(QUESTION_BANK):
    q = QUESTION_BANK[st.session_state.bm_step]

    st.subheader(f"{q['section']} • Question {st.session_state.bm_step + 1} of {len(QUESTION_BANK)}")
    st.markdown(f"**{q['text']}**")

    # restore previous selection if user navigated back
    prev = st.session_state.bm_answers.get(q["id"], None)
    options = list(q["options"].keys())
    if prev and prev in options:
        default_index = options.index(prev)
    else:
        default_index = 0

    choice = st.radio(
        "Choose one:",
        options,
        index=default_index,
        label_visibility="collapsed",
        key=f"bm_q_{q['id']}"
    )

    c1, c2 = st.columns([1,1])
    with c1:
        st.button("⬅ Back", on_click=go_back, use_container_width=True, disabled=(st.session_state.bm_step == 0))
    with c2:
        st.button("Next ➜", on_click=lambda: go_next(choice), use_container_width=True)

# -------- Results --------
else:
    # accumulate tags from answers
    base_weights: Counter = accumulate_tags(st.session_state.bm_answers)

    # apply TRL adjustments if available
    adjusted_weights = trl_gate_score_adjustments(base_weights, trl)

    # load & score models
    models = load_models()
    top3 = score_models(adjusted_weights, models, top_k=3)

    st.success(f"✅ Questionnaire complete! We computed {sum(abs(v) for v in adjusted_weights.values())} weighted signals.")
    st.markdown("### 🏆 Top Recommendations")

    names_for_next = []
    for i, item in enumerate(top3, start=1):
        m = item["model"]
        names_for_next.append(m["name"])
        st.markdown(f"**{i}. {m['name']}** — Score: `{item['score']}`")
        st.caption(m.get("description", ""))

        with st.expander("Why this model? (Matched tags)"):
            if item["matched"]:
                st.write({k: v for k, v in item["matched"].items()})
            else:
                st.write("No strong positive tag matches — consider adjacent models too.")

        if item["penalties"]:
            with st.expander("Where it may not fit (penalties)"):
                st.write(item["penalties"])

    st.divider()
    st.markdown("###Export to next steps")
    if names_for_next:
        sel = st.selectbox("Choose one for Financial Projection / Roadmap", names_for_next, index=0)
        st.session_state["top3_models"] = names_for_next
        st.session_state["selected_model"] = sel
        st.success(f"Saved selection: **{sel}** → Now open: Financial Projection / Road-to-Market pages.")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔁 Restart", on_click=restart, use_container_width=True):
            pass
    with c2:
        st.page_link("pages/03_Financial_Projection.py", label="➡ Go to Financial Projection", icon="💰")

