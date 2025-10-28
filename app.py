# app.py
import streamlit as st
from utils.trl_logic import questions, calculate_trl, trl_description

st.set_page_config(page_title="TRL Calculator", page_icon="🧪", layout="centered")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = []

def next_step(answer):
    st.session_state.answers.append(answer)
    st.session_state.step += 1

# Header
st.title("🧪 Technology Readiness Level (TRL) Calculator")
st.caption("A guided 9-step questionnaire to determine your technology maturity level.")

# Progress
progress = st.session_state.step / len(questions)
st.progress(progress)

# Main logic
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
    trl = calculate_trl(st.session_state.answers)
    st.success(f"Your estimated TRL is **{trl} / 9**")
    st.markdown(f"**Description:** {trl_description(trl)}")

    # Suggestion for next stage
    if trl < 9:
        st.info(f"To reach **TRL {trl+1}**, focus on: validating and demonstrating your system in its next relevant environment.")
    else:
        st.balloons()
        st.success("🎉 Congratulations! You’ve reached TRL 9 — proven commercial operation.")

    if st.button("🔁 Restart"):
        st.session_state.step = 0
        st.session_state.answers = []
