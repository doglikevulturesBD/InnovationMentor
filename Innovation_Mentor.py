import streamlit as st

st.set_page_config(
    page_title="Innovation Mentor",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------
# Header Section
# ---------------------------
st.title("🚀 Innovation Mentor Platform")
st.caption("Integrated framework for innovators — from TRL assessment to commercialization readiness.")

st.markdown("""
Welcome to the **Innovation Mentor App**, your one-stop tool for guiding technology projects
from early research to market-ready commercialization.  
Use the sidebar to navigate through each stage of development:
""")

# ---------------------------
# Quick Navigation Cards
# ---------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.header("📊 Assessment")
    st.page_link("pages/01_TRL_Calculator.py", label="TRL Calculator", icon="🧪")
    st.page_link("pages/02_Business_Model_Selector.py", label="Business Model Selector", icon="🏗️")
    st.page_link("pages/03_Financial_Projection.py", label="Financial Projection", icon="💰")
    st.page_link("pages/04_DCF_IRR_NPV.py", label="DCF / IRR / NPV", icon="📈")

with col2:
    st.header("📚 Market & Strategy")
    st.page_link("pages/05_Market_Study_Guide.py", label="Market Study Guide", icon="🧭")
    st.page_link("pages/06_Marketing_Strategy.py", label="Marketing Strategy", icon="📢")
    st.page_link("pages/09_Financing_Options.py", label="Financing Options", icon="🏦")
    st.page_link("pages/08_IP_Management.py", label="IP Management", icon="🧩")

with col3:
    st.header("🧠 Advanced Tools")
    st.page_link("pages/10_MonteCarlo_Scenarios.py", label="Monte Carlo Simulator", icon="🎲")
    st.page_link("pages/11_Risk_Dashboard.py", label="Risk Dashboard", icon="⚠️")
    st.page_link("pages/12_Road_to_Market.py", label="Road-to-Market", icon="🛣️")
    st.page_link("pages/07_Export_Report.py", label="Export Summary", icon="📤")

# ---------------------------
# Footer
# ---------------------------
st.divider()
st.info("""
💡 **Tip:** Start with the TRL Calculator to determine your technology maturity level.  
Based on your TRL, the app will later filter suitable business models, financing types, and commercialization paths.
""")

