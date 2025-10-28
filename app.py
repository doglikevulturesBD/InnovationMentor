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
st.caption("Answer the guided 9-step questionnaire to find your current TRL and next milestones.")

# --- Progress bar ---
progress = st.session_state.step / len(questions)
st.progress(progress)

# --- Questionnaire Flow ---
if not st.session_state.done and st.session_state.step < len(questions):
    q = questions[st.session_state.step]
    st.subheader(f"Step {st.session_state.step + 1} of {len(questions)}")
    st.markdown(f"**{q['text']}**")

    choice = st.radio(
        "Select your answer:",
        ["Yes", "No"],
        key=f"q_{st.session_state.step}",
        horizontal=True,
        label_visibility="collapsed"
    )

    if st.button("Next ➜"):
        st.session_state.answers.append(choice == "Yes")
        if choice == "No":
            st.session_state.done = True  # Stop immediately
        else:
            st.session_state.step += 1
            if st.session_state.step == len(questions):
                st.session_state.done = True
        st.rerun()  # Forces Streamlit to refresh state immediately

# --- Results ---
elif st.session_state.done:
    trl = calculate_trl(st.session_state.answers)
    st.success(f"Your estimated TRL is **{trl} / 9**")
    st.markdown(f"### 🔍 Description: {trl_description(trl)}")

    if trl < 9:
        st.info(f"To reach **TRL {trl + 1}**, focus on:\n\n> {trl_descriptions[trl + 1]}")
    else:
        st.balloons()
        st.success("🎉 TRL 9 achieved — your system is proven in commercial operation!")

    st.divider()
    st.markdown("### 📊 TRL Reference Overview")
    for lvl, desc in trl_descriptions.items():
        highlight = "🟩" if lvl == trl else "⬜"
        st.markdown(f"{highlight} **TRL {lvl}:** {desc}")

    if st.button("🔁 Restart"):
        st.session_state.step = 0
        st.session_state.answers = []
        st.session_state.done = False
        st.rerun()

