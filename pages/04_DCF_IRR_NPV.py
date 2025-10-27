
import streamlit as st
from utils.finance import npv, irr, payback_period
st.title("DCF / IRR / NPV")
discount = st.slider("Discount rate (%)", 0, 40, 15)
proj = st.session_state.get("projection", {"net_cf":[-100000, 30000, 40000, 50000]})
cfs = proj["net_cf"]
st.metric("NPV (R)", f"{npv(discount/100.0, cfs):,.0f}")
st.metric("IRR", f"{irr(cfs)*100:,.1f}%")
st.metric("Payback (years)", f"{payback_period(cfs):.2f}")
st.session_state["finance_snapshot"] = {"npv": round(npv(discount/100.0, cfs),2), "irr": f"{irr(cfs)*100:.1f}%", "payback": round(payback_period(cfs),2)}
