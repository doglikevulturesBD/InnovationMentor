import streamlit as st
from utils.reflections_store import save_reflection


def enforce_reflection(module_name: str):
    """
    Tracks full page uses of each module.
    After 3 full uses, the user must complete a reflection before continuing.
    Reflections are saved privately (not visible in public comments).
    """

    # --- Session Keys ---
    use_key = f"use_count_{module_name}"
    reflection_required_key = f"reflection_required_{module_name}"
    reflection_ack_key = f"reflection_acknowledged_{module_name}"

    # --- Initialise State ---
    st.session_state.setdefault(use_key, 0)
    st.session_state.setdefault(reflection_required_key, False)
    st.session_state.setdefault(reflection_ack_key, False)

    # --- Count FULL MODULE USE ---
    # (Only count if a reflection is not currently required)
    if not st.session_state[reflection_required_key]:
        st.session_state[use_key] += 1

    # --- Trigger reflection requirement after 3 full uses ---
    if st.session_state[use_key] >= 3 and not st.session_state[reflection_required_key]:
        st.session_state[reflection_required_key] = True

    # --- BLOCK PAGE IF REFLECTION REQUIRED ---
    if st.session_state[reflection_required_key] and not st.session_state[reflection_ack_key]:

        st.error("Reflection required before continuing 👇")
        st.subheader("Mandatory Reflection / Suggestion")

        reflection_text = st.text_area(
            "Before continuing, please write one quick suggestion, lesson learned, or next step:",
            height=130
        )

        if st.button("Submit Reflection"):
            if len(reflection_text.strip()) == 0:
                st.warning("Please enter something meaningful before submitting.")
            else:
                # Save reflection privately
                save_reflection(module_name, reflection_text.strip())

                # Reset counters + flags
                st.session_state[use_key] = 0
                st.session_state[reflection_required_key] = False
                st.session_state[reflection_ack_key] = True

                st.success("Reflection submitted. You may now continue.")
                st.rerun()

        # HARD BLOCK — stop all module content
        st.stop()

    # --- Allow normal use after user completed reflection ---
    if st.session_state[reflection_ack_key]:
        # Reset acknowledgement so the next cycle works cleanly
        st.session_state[reflection_ack_key] = False

    # --- Optional progress indicator ---
    progress = min(st.session_state[use_key] / 3, 1.0)
    st.progress(progress)

