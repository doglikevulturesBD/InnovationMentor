import streamlit as st

def admin_comment_manager(module_name):
    key = f"comments_{module_name}"

    st.subheader("Admin Comment Management")

    if key not in st.session_state or st.session_state[key] == "":
        st.info("No public comments for this module yet.")
        return

    st.text_area("Current Public Comment:", value=st.session_state[key], height=140, disabled=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Delete Comment"):
            del st.session_state[key]
            st.success("Comment deleted.")
            st.rerun()

    with col2:
        if st.button("Clear Comment Without Deleting"):
            st.session_state[key] = ""
            st.success("Comment cleared.")
            st.rerun()

