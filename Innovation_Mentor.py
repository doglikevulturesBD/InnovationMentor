import streamlit as st
from utils.access_control import login_screen, logout_button

st.set_page_config(page_title="Innovation Mentor", page_icon="💡", layout="wide")

# ----------------------------
# LOGIN GATE
# ----------------------------
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    login_screen()
    st.stop()

# ----------------------------
# POST-LOGIN INTERFACE
# ----------------------------
st.sidebar.title("💡 Innovation Mentor")
st.sidebar.caption(f"Logged in as: {st.session_state.user} ({st.session_state.role})")
logout_button()

role = st.session_state.role

st.title("Welcome to the Innovation Mentor Platform")

if role == "Admin":
    st.success("You are in Admin mode. Full functionality enabled.")
    st.write("Access to all tools, editors, and data export options.")

elif role == "Evaluator":
    st.info("You are in Evaluator mode (read-only). Some editing is disabled.")
    st.write("You can review project data but cannot modify entries.")

elif role == "Demo":
    st.warning("You are in Demo mode. Limited sections available.")
    st.write("Use this mode to explore TRL, Business Model, and Commercialisation only.")

st.markdown("---")
st.markdown("### Quick Access Links")
if role == "Admin":
    st.markdown("- [TRL Assessment](./01_TRL_Assessment)")
    st.markdown("- [Business Model](./02_Business_Model)")
    st.markdown("- [Financial Projections](./03_Financial_Projection)")
    st.markdown("- [IP Management](./04_IP_Management)")
    st.markdown("- [Commercialisation Strategy](./05_Commercialisation_Strategy)")
    st.markdown("- [Risk Dashboard](./06_Risk_Dashboard)")
elif role == "Evaluator":
    st.markdown("- [TRL Assessment](./01_TRL_Assessment)")
    st.markdown("- [Business Model](./02_Business_Model)")
    st.markdown("- [Commercialisation Strategy](./05_Commercialisation_Strategy)")
    st.markdown("- [Risk Dashboard](./06_Risk_Dashboard)")
elif role == "Demo":
    st.markdown("- [TRL Assessment](./01_TRL_Assessment)")
    st.markdown("- [Business Model](./02_Business_Model)")
    st.markdown("- [Commercialisation Strategy](./05_Commercialisation_Strategy)")
