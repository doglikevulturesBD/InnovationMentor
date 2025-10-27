
import streamlit as st

st.set_page_config(page_title="Commercialisation Mentor", page_icon="🧭", layout="wide")

st.title("🧭 Commercialisation Mentor — Demo")
st.markdown("Welcome! Step through TRL → Business Model → Finance → Risk → Roadmap → Export.")
st.page_link("pages/01_TRL_Calculator.py", label="1) TRL Calculator")
st.page_link("pages/02_Business_Model_Selector.py", label="2) Business Model Selector")
st.page_link("pages/03_Financial_Projection.py", label="3) Financial Projection")
st.page_link("pages/04_DCF_IRR_NPV.py", label="4) DCF / IRR / NPV")
st.page_link("pages/05_Market_Study_Guide.py", label="5) How to do a Market Study")
st.page_link("pages/06_Marketing_Strategy.py", label="6) Marketing Strategy")
st.page_link("pages/07_Export_Report.py", label="7) Export PDF/Markdown")
st.page_link("pages/08_IP_Management.py", label="8) IP Types & Management Strategy")
st.page_link("pages/09_Financing_Options.py", label="9) Financing Options")
st.page_link("pages/10_MonteCarlo_Scenarios.py", label="10) Monte Carlo — NPV Scenarios")
st.page_link("pages/11_Risk_Dashboard.py", label="11) Risk & Feasibility Dashboard")
st.page_link("pages/12_Road_to_Market.py", label="12) Road-to-Market Generator")
