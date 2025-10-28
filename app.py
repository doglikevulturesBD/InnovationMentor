import streamlit as st
from utils.trl_logic import questions, calculate_trl, trl_description, trl_descriptions

st.set_page_config(page_title="TRL Calculator", page_icon="🧪", layout="centered")

# --- Initialize session state ---
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "done" not in st.session_state:
    st.session_state.done = False

# --- Header ---
st.title("🧪 Technology Readiness Level (TRL) Calculator")
st.caption("Answer the questions step-by-step to estimate your technology maturity level.")

# --- Progress bar ---
progress = st.session_state.step / len(questions)
st.progress(progress)

# --- Questionnaire Flow ---
if not st.session_state.done and st.session_state.step < len(questions):
    q = questions[st.session_state.step]
    st.subheader(f"Step {st.session_state.step + 1} of {len(questions)}")
    st.markdown(f"**{q['text']}**")

    col1, col2 = st.columns(2)

    # Use form to prevent double-click issue
    with st.form(key=f"form_{st.session_state.step}"):
        submit_yes = st.form_submit_button("✅ Yes")
        submit_no = st.form_submit_button("❌ No")

    if submit_yes:
        st.session_state.answers.append(True)
        st.session_state.step += 1
        if st.session_state.step == len(questions):
            st.session_state.done = True

    elif submit_no:
        st.session_state.answers.append(False)
        st.session_state.done = True  # Stop questionnaire immediately

# --- Result Section ---
elif st.session_state.done:
    trl = calculate_trl(st.session_state.answers)
    st.success(f"Your estimated TRL is **{trl} / 9**")
    st.markdown(f"### 🔍 Description: {trl_description(trl)}")

    if trl < 9:
        st.info(f"To reach **TRL {trl + 1}**, focus on the next stage:\n\n> {trl_descriptions[trl + 1]}")
    else:
        st.balloons()
        st.success("🎉 You’ve reached TRL 9: proven commercial operation in intended environment.")

    # Show all levels for reference
    st.markdown("### 📊 TRL Overview")
    for lvl, desc in trl_descriptions.items():
        prefix = "👉" if lvl == trl else ""
        st.markdown(f"{prefix} **TRL {lvl}:** {desc}")

    # Restart button
    if st.button("🔁 Restart Questionnaire"):
        st.session_state.step = 0
        st.session_state.answers = []
        st.session_state.done = False
