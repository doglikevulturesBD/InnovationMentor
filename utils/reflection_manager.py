import streamlit as st

def enforce_reflection(module_name: str):

    # Keys
    use_key = f"use_count_{module_name}"
    reflection_key = f"reflection_required_{module_name}"
    acknowledged_key = f"reflection_acknowledged_{module_name}"

    # Initialise
    st.session_state.setdefault(use_key, 0)
    st.session_state.setdefault(reflection_key, False)
    st.session_state.setdefault(acknowledged_key, False)

    # Count a full use ONLY if reflection is not pending
    if not st.session_state[reflection_key]:
        st.session_state[use_key] += 1

    # Trigger reflection after 3 full uses
    if st.session_state[use_key] >= 3 and not st.session_state[reflection_key]:
        st.session_state[reflection_key] = True

    # If reflection is required → block the page until completed
    if st.session_state[reflection_key] and not st.session_state[acknowledged_key]:
        st.error("Reflection required before continuing 👇")
        st.subheader("Required Reflection / Suggestion")

        response = st.text_area(
            "Please write one suggestion, lesson, or improvement before continuing:",
            height=130
        )

        if st.button("Submit Reflection"):
            if len(response.strip()) == 0:
                st.warning("Please enter something meaningful before submitting.")
            else:
                # Reset everything
                st.session_state[use_key] = 0
                st.session_state[reflection_key] = False
                st.session_state[acknowledged_key] = True

                st.success("Reflection saved! You may now continue using this module.")
                st.rerun()

        # Hard block the module until completed
        st.stop()

    # Allow normal use if reflection is done
    if st.session_state[acknowledged_key]:
        # After the first click through, allow new cycles again
        st.session_state[acknowledged_key] = False

    # Progress bar (optional)
    st.progress(min(st.session_state[use_key] / 3, 1.0))

