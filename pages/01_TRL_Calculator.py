# app.py
import streamlit as st
from utils.reflection_manager import enforce_reflection
from utils.comments_manager import comments_box
from utils.trl_logic import (
    questions, calculate_trl, trl_description,
    trl_descriptions, next_trl_description
)

module_name = "TRL_Assessment"
enforce_reflection(module_name)

st.title("TRL Assessment Tool")

# ---------- Session State ----------
if "step" not in st.session_state:        st.session_state.step = 0
if "answers" not in st.session_state:     st.session_state.answers = []
if "finished" not in st.session_state:    st.session_state.finished = False

def handle_answer(answer: bool):
    """Single-click safe: called by on_click of Yes/No buttons."""
    st.session_state.answers.append(answer)
    if not answer:
        # Stop immediately on 'No'
        st.session_state.finished = True
        return
    # Advance to next step or finish if last
    st.session_state.step += 1
    if st.session_state.step >= len(questions):
        st.session_state.finished = True

def restart():
    st.session_state.step = 0
    st.session_state.answers = []
    st.session_state.finished = False




# ---------- Progress ----------
progress = st.session_state.step / len(questions)
st.progress(progress)

# ---------- Flow ----------
if not st.session_state.finished and st.session_state.step < len(questions):
    q = questions[st.session_state.step]
    st.subheader(f"Step {st.session_state.step + 1} of {len(questions)}")
    st.markdown(f"**{q['text']}**")

    col1, col2 = st.columns(2)
    col1.button("✅ Yes", key=f"yes_{st.session_state.step}", use_container_width=True,
                on_click=handle_answer, args=(True,))
    col2.button("❌ No", key=f"no_{st.session_state.step}", use_container_width=True,
                on_click=handle_answer, args=(False,))

else:
    # Finished or reached the end
    trl = calculate_trl(st.session_state.answers)
    label = "TRL 0 (pre-TRL)" if trl == 0 else f"TRL {trl} / 9"
    st.success(f"Your estimated level: **{label}**")

    st.markdown("### 🔍 What this means")
    st.write(trl_description(trl))

    if trl < 9:
        st.info(f"**Next target — TRL {trl + 1}:** {next_trl_description(trl)}")
    else:
        st.balloons()
        st.success("🎉 TRL 9 achieved — proven commercial operation!")

    st.divider()
    st.markdown("### 📘 TRL Reference Overview")
    # Show from 0 (pre-TRL) through 9, highlighting current
    for lvl in range(0, 10):
        if lvl not in trl_descriptions: 
            continue
        marker = "🟩" if lvl == trl else "⬜"
        title = "TRL 0 (pre-TRL)" if lvl == 0 else f"TRL {lvl}"
        st.markdown(f"{marker} **{title}:** {trl_descriptions[lvl]}")

    st.button("🔁 Restart", on_click=restart, use_container_width=True)
# Optional comments section
comments_box(module_name)
