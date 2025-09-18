import streamlit as st

st.set_page_config(page_title="Innovation Mentor", layout="wide")

st.sidebar.title("🧭 Innovation Mentor")
section = st.sidebar.radio("Navigate to:", ["🌱 Idea Stage", "⚙️ Development Stage", "🚀 Launch Stage"])

st.title("💡 Innovation Mentor App")
st.markdown("""
Welcome to your personal **Innovation Mentor** — a tool to guide innovators through the journey 
from **idea to impact**.  
Use the sidebar to explore each stage.
""")

if section == "🌱 Idea Stage":
    st.switch_page("pages/1_Idea_Stage.py")

elif section == "⚙️ Development Stage":
    st.switch_page("pages/2_Development_Stage.py")

elif section == "🚀 Launch Stage":
    st.switch_page("pages/3_Launch_Stage.py")
