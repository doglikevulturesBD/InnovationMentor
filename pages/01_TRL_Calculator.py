import streamlit as st
from utils.trl_logic import questions, calculate_trl, trl_description

st.set_page_config(page_title="TRL Calculator", page_icon="🧪", layout="centered")

# --- Initialize session state ---
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = []

# --- Helper to move to next question ---
def next_step(answer):
    st.session_state.answers.append(answer)
    st.session_state.step += 1

# --- Header ---
st.title("🧪 TRL Calculator")
st.caption("Estimate your Technology Readiness Level through a guided 7-step questionnaire")

# --- Progress bar ---
progress = st.session_state.step / len(questions)
st.progress(progress)

# --- Question flow ---
if st.session_state.step < len(questions):
    q = questions[st.session_state.step]
    st.subheader(f"Step {st.session_state.step+1} of {len(questions)}")
    st.markdown(f"**{q['text']}**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Yes", key=f"yes_{st.session_state.step}"):
            next_step(True)
    with col2:
        if st.button("❌ No", key=f"no_{st.session_state.step}"):
            next_step(False)

else:
    # --- Calculate TRL ---
    trl = calculate_trl(st.session_state.answers)
    st.success(f"Your estimated TRL is **{trl}**")
    st.markdown(f"**Description:** {trl_description(trl)}")

    if st.button("🔁 Restart"):
        st.session_state.step = 0
        st.session_state.answers = []
