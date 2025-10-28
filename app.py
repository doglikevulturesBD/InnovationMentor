import streamlit as st
from utils.trl_logic import questions, calculate_trl, trl_description, trl_descriptions

st.set_page_config(page_title="TRL Calculator", page_icon="🧪", layout="centered")

# --- Initialize state ---
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "finished" not in st.session_state:
    st.session_state.finished = False

# --- App Header ---
st.title("🧪 Technology Readiness Level (TRL) Calculator")
st.caption("Answer the questions step-by-step. The questionnaire will stop once you answer 'No'.")

# --- Progress bar ---
progress = st.session_state.step / len(questions)
st.progress(progress)

# --- Questionnaire flow ---
if not st.session_state.finished and st.session_state.step < len(questions):
    q = questions[st.session_state.step]
    st.subheader(f"Step {st.session_state.step + 1} of {len(questions)}")
    st.markdown(f"**{q['text']}**")

    col1, col2 = st.columns(2)
    yes = col1.button("✅ Yes", key=f"yes_{st.session_state.step}")
    no = col2.button("❌ No", key=f"no_{st.session_state.step}")

    if yes:
        st.session_state.answers.append(True)
        st.session_state.step += 1
        st.rerun()

    elif no:
        st.session_state.answers.append(False)
        st.session_state.finished = True
        st.rerun()

# --- Result Section ---
elif st.session_state.finished or st.session_state.step >= len(questions):
    trl = calculate_trl(st.session_state.answers)
    st.success(f"Your estimated TRL is **{trl} / 9**")
    st.markdown(f"### 🔍 Description\n{trl_description(trl)}")

    # Show the next TRL level
    if trl < 9:
        st.info(f"**To reach TRL {trl + 1}:**\n\n{trl_descriptions[trl + 1]}")
    else:
        st.balloons()
        st.success("🎉 You have achieved TRL 9 — proven commercial operation!")

    st.divider()
    st.markdown("### 📘 TRL Reference Overview")
    for lvl, desc in trl_descriptions.items():
        highlight = "🟩" if lvl == trl else "⬜"
        st.markdown(f"{highlight} **TRL {lvl}:** {desc}")

    if st.button("🔁 Restart"):
        st.session_state.step = 0
        st.session_state.answers = []
        st.session_state.finished = False
        st.rerun()

