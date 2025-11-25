import streamlit as st
from utils.reflection_manager import enforce_reflection
from utils.comments_manager import comments_box
from utils.trl_logic import (
    questions, calculate_trl, trl_description,
    trl_descriptions, next_trl_description
)

st.title("🚦 TRL Assessment Tool")
st.caption("Answer each question honestly. A single ‘No’ will stop the assessment and assign the appropriate TRL.")

# ---------- Session State ----------
if "step" not in st.session_state:        st.session_state.step = 0
if "answers" not in st.session_state:     st.session_state.answers = []
if "finished" not in st.session_state:    st.session_state.finished = False

def handle_answer(answer: bool):
    st.session_state.answers.append(answer)
    if not answer:
        st.session_state.finished = True
        return
    st.session_state.step += 1
    if st.session_state.step >= len(questions):
        st.session_state.finished = True

def restart():
    st.session_state.step = 0
    st.session_state.answers = []
    st.session_state.finished = False


# Sidebar reset
with st.sidebar:
    st.header("TRL Tool")
    if st.button("🔄 Restart Assessment"):
        restart()
        st.experimental_rerun()


# ---------- Progress ----------
progress = st.session_state.step / len(questions)
st.progress(progress)

# ---------- Flow ----------
if not st.session_state.finished and st.session_state.step < len(questions):
    q = questions[st.session_state.step]
    st.markdown(f"### Step {st.session_state.step + 1} / {len(questions)}")
    st.markdown(f"**{q['text']}**")

    col1, col2 = st.columns(2)
    col1.button("🟩 Yes", key=f"yes_{st.session_state.step}", use_container_width=True,
                on_click=handle_answer, args=(True,))
    col2.button("🟥 No", key=f"no_{st.session_state.step}", use_container_width=True,
                on_click=handle_answer, args=(False,))

else:
    trl = calculate_trl(st.session_state.answers)
    label = "TRL 0 (pre-TRL)" if trl == 0 else f"TRL {trl} / 9"

    st.success(f"### 🎯 Your Technology Readiness Level: **{label}**")

    st.markdown("### 🔍 What This Means")
    st.write(trl_description(trl))

    st.markdown("### 📝 Your Responses")
    for i, ans in enumerate(st.session_state.answers):
        mark = "🟩 Yes" if ans else "🟥 No"
        st.write(f"**Step {i+1}:** {mark}")

    if trl < 9:
        st.markdown("### 🛠 How to Reach the Next TRL")
        st.info(f"**TRL {trl + 1}:** {next_trl_description(trl)}")
    else:
        st.balloons()
        st.success("🎉 TRL 9 achieved — proven commercial operation!")

    st.divider()
    st.markdown("### 📘 TRL Reference Overview")
    for lvl in range(0, 10):
        if lvl not in trl_descriptions: 
            continue
        marker = "🟩" if lvl == trl else "⬜"
        title = "TRL 0 (pre-TRL)" if lvl == 0 else f"TRL {lvl}"
        st.markdown(f"{marker} **{title}:** {trl_descriptions[lvl]}")

    st.markdown("### 💬 Reflection")
    enforce_reflection("trl_assessment")

    st.button("🔁 Restart", on_click=restart, use_container_width=True)

