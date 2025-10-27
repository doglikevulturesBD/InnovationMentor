
import streamlit as st
from utils.finance import build_projection

st.title("Financial Projection (10 years)")
model = st.session_state.get("selected_model","SaaS Subscription")
st.info(f"Selected business model: **{model}**")
years = st.number_input("Projection years", 5, 20, 10)
base_revenue = st.number_input("Year 1 revenue (R)", min_value=0.0, value=250000.0, step=5000.0, format="%.2f")
growth = st.slider("Annual revenue growth (%)", 0, 100, 35)
opex_ratio = st.slider("OPEX as % of revenue", 0, 100, 45)
capex_y1 = st.number_input("Capex Year 1 (R)", min_value=0.0, value=150000.0, step=5000.0, format="%.2f")
capex_follow = st.number_input("Capex Year 2+ (R per year)", min_value=0.0, value=20000.0, step=1000.0, format="%.2f")
revenue, opex, capex = [], [], []
r = base_revenue
for y in range(int(years)):
    revenue.append(r); opex.append(r*(opex_ratio/100.0)); capex.append(capex_y1 if y==0 else capex_follow); r *= (1 + growth/100.0)
proj = build_projection(int(years), revenue, opex, capex, tax_rate=0.28, depreciation_years=5)
st.subheader("Net Cashflows")
st.line_chart(proj["net_cf"])
st.session_state["projection"] = proj
