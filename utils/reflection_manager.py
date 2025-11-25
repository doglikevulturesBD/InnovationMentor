import streamlit as st

def enforce_reflection(module_name: str):
    """
    Blocks the user after 3 uses of a module until they complete a reflection.
    After reflection is submitted, usage resets and user may continue indefinitely.
    """

    use_key = f"use_count_{module_name}"
    reflection_key = f"reflection_done_{module_name}"

    # Initialise keys
    st.session_state.setdefault(use_key, 0)
    st.session_state.setdefault(reflection_key, False)

    # Only increment usage if reflection is not pending
    if not st.session_state[reflection_key]:
        st.session_state[use_key] += 1

    # If 3 uses → require reflection
    if st.session_state[use_key] >= 3 and not st.session_state[reflection_key]:
        st.error("Reflection required before continuing 👇")

        st.subheader("Reflection / Suggestion Before Continuing")
        response = st.text_area(
            "Write a short suggestion, insight, or next step:",
            height=130
        )

        if st.button("Submit Reflection"):
            if len(response.strip()) == 0:
                st.warning("Please enter something before submitting.")
            else:
                st.session_state[reflection_key] = True
                st.session_state[use_key] = 0
                st.success("Thank you — you can now continue using this module.")
                st.rerun()

        # Stop page until reflection is done
        st.stop()

    # Optional progress indicator
    progress = min(st.session_state[use_key] / 3, 1.0)
    st.progress(progress)
