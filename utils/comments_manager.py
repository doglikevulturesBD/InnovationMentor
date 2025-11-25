import streamlit as st

def comments_box(module_name: str):
    """
    Optional comments/notes box.
    Does not affect the reflection requirement.
    """

    comment_key = f"comments_{module_name}"

    st.markdown("---")
    st.subheader("Optional Notes / Comments")

    existing = st.session_state.get(comment_key, "")

    new_text = st.text_area(
        "Add a comment (optional):",
        value=existing,
        height=140
    )

    if st.button("Save Comment"):
        st.session_state[comment_key] = new_text
        st.success("Comment saved.")
