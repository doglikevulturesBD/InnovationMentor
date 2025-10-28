# pages/02_Business_Model_Selector.py
import streamlit as st
from utils.model_logic import questions, load_models, score_models

st.set_page_config(page_title="Business Model Selector", page_icon="🏗️", layout="centered")

# --- Initialize session state ---
if "bm_step" not in st.session_state:
    st.session_state.bm_step = 0
if "bm_answers" not in st.session_state:
    st.session_state.bm_answers = {}
if "bm_done" not in st.session_state:
    st.session_state.bm_done = False

st.title("🏗️ Business Model Selector")
st.caption("Answer short questions to discover the best-fit business models for your innovation.")

# --- Questionnaire ---
if not st.session_state.bm_done and st.session_state.bm_step < len(questions):
    q = questions[st.session_state.bm_step]
    st.subheader(f"Question {st.session_state.bm_step + 1} of {len(questions)}")
    st.markdown(f"**{q['text']}**")

    col1, col2 = st.columns(2)
    yes = col1.button("✅ Yes", key=f"yes_{st.session_state.bm_step}")
    no = col2.button("❌ No", key=f"no_{st.session_state.bm_step}")

    if yes:
        st.session_state.bm_answers[q["tag_yes"]] = True
        st.session_state.bm_step += 1
        st.rerun()

    elif no:
        st.session_state.bm_step += 1
        st.rerun()

# --- Results ---
elif st.session_state.bm_done or st.session_state.bm_step >= len(questions):
    selected_tags = set(st.session_state.bm_answers.keys())
    models = load_models()
    top3 = score_models(selected_tags, models)

    st.success(f"✅ Questionnaire complete! You matched **{len(selected_tags)}** characteristics.")
    st.markdown("### 🏆 Top 3 Recommended Business Models")

    for i, item in enumerate(top3, 1):
        m = item["model"]
        st.markdown(f"**{i}. {m['name']}** — Score: {item['score']}")
        st.caption(f"Tags matched: {', '.join(set(m.get('tags', [])) & selected_tags)}")
        with st.expander("View details"):
            st.write(m["description"])

    st.divider()
    st.button("🔁 Restart", on_click=lambda: [st.session_state.update({"bm_step": 0, "bm_answers": {}, "bm_done": False}), st.rerun()])

