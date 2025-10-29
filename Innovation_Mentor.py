import streamlit as st
from utils.access_control import login

st.set_page_config(page_title="Innovation Mentor", page_icon="💡", layout="wide")

st.title("💡 Innovation Mentor App")

role = login()

# --- Role-based access control ---
if role == "Admin":
    st.success("Welcome, Admin! You have full access to all modules.")
    st.sidebar.write("Access: All sections enabled.")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📚 Full Modules:")
    st.sidebar.write("TRL, Business Model, Financials, IP, Commercialisation, Risk, etc.")
    st.markdown("Use the sidebar or page menu to explore all sections.")

elif role == "Evaluator":
    st.info("Welcome, Evaluator! You can view all pages but with limited edit capability.")
    st.sidebar.write("Access: Read-only mode.")
    st.sidebar.markdown("You can navigate the full app but some input widgets will be disabled.")

elif role == "Demo":
    st.warning("Welcome to the Demo Version! Limited access is active.")
    st.sidebar.write("Access: TRL, Business Model, and Commercialisation only.")
    st.sidebar.markdown("Use these pages to preview app features.")
    st.markdown("""
    ### Demo Overview
    This version allows:
    - TRL Assessment
    - Business Model Selection
    - Commercialisation & Marketing Strategy
    - Partial Risk Dashboard (Preview)
    """)
else:
    st.error("Something went wrong — please try logging in again.")
