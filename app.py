# app.py (replace the whole file if easier)

import streamlit as st
from utils.trl_logic import questions, calculate_trl, trl_description, trl_descriptions

st.set_page_config(page_title="TRL Calculator", page_icon="🧪", layout="centered")

if "step" not in st.session_state: st.session_state.step = 0
if "answers" not in st.session_state: st.session_state.answers = []
if "done" not in st.session_state: st.session_state.done = False

st.title("🧪 Technology Readiness Level (TRL) Calculator")
st.caption("Linear, stop-on-No questionnaire. Your TRL is the count of consecutive 'Yes' from TRL1 upward.")

progress = st.session_state.step / len(questions)
st.progress(progress)

def reset_radio_key():
    key = f"q_{st.session_state.step}"
    if key in st.session_state:
        del st.session_state[key]

# Flow
if not st.session_state.done and st.session_state.step < len(questions):
    q = questions[st.session_state.step]
    st.subheader(f"Step {st.session_state.step + 1} of {len(questions)}")
    st.markdown(f"**{q['text']}**")

    choice = st.radio(
        "Select your answer:",
        ["Yes", "No"],
        key=f"q_{st.session_state.step}",
        horizontal=True,
        label_visibility="collapsed",
        index=0  # default to Yes so users can move fast if appropriate
    )

    if st.button("Next ➜", use_container_width=True):
        st.session_state.answers.append(choice == "Yes")
        if choice == "No":
            st.session_state.done = True
        else:
            st.session_state.step += 1
            if st.session_state.step == len(questions):
                st.session_state.done = True
        reset_radio_key()
        st.rerun()

else:
    trl = calculate_trl(st.session_state.answers)
    st.success(f"Your estimated TRL is **{trl} / 9**")
    st.markdown(f"### 🔍 What this means\n{trl_description(trl)}")

    # Next milestone
    if trl < 9:
        nxt = trl + 1
        st.info(f"**Next target — TRL {nxt}:** {trl_descriptions[nxt]}")
    else:
        st.balloons()
        st.success("🎉 TRL 9 achieved — proven commercial operation!")

    st.divider()
    st.markdown("### 📊 TRL Reference Overview")
    for lvl in range(0, 10):  # include TRL 0 row
        if lvl not in trl_descriptions: continue
        mark = "🟩" if lvl == trl else "⬜"
        st.markdown(f"{mark} **TRL {lvl}:** {trl_descriptions[lvl]}")

    if st.button("🔁 Restart", use_container_width=True):
        st.session_state.step = 0
        st.session_state.answers = []
        st.session_state.done = False
        st.rerun()
