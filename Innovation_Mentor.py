import streamlit as st

st.set_page_config(page_title="Innovation Mentor Launchpad", layout="wide")

st.title("🚀 Innovation Mentor Launchpad")
st.markdown("""
Welcome to your personal **Innovation Mentor** — a tool to guide innovators through the journey 
from **idea to impact**.

Select a stage below to begin exploring.
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🌱 Idea Stage")
    st.markdown("**Explore how to shape and validate your early ideas.**")
    if st.button("Go to Idea Stage", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Idea_Stage.py")

with col2:
    st.markdown("### ⚙️ Development Stage")
    st.markdown("**Turn your validated idea into a product or service.**")
    if st.button("Go to Development Stage", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Development_Stage.py")

with col3:
    st.markdown("### 🚀 Launch Stage")
    st.markdown("**Prepare for market entry, scaling, and impact.**")
    if st.button("Go to Launch Stage", use_container_width=True, type="primary"):
        st.switch_page("pages/3_Launch_Stage.py")
