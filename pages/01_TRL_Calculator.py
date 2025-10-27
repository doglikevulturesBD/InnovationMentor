
import streamlit as st
st.title("TRL Calculator")
st.write("Estimate a simple TRL for MVP purposes.")
st.number_input("Successful prototype tests", 0, 100, 0, key="trl_tests")
st.selectbox("Field tested with real users?", ["No","Pilot","Yes"], key="trl_field")
st.selectbox("Manufacturing/Delivery process defined?", ["No","Partial","Yes"], key="trl_mfg")
def estimate_trl():
    base = 3
    if st.session_state.trl_tests >= 1: base = 4
    if st.session_state.trl_field == "Pilot": base = max(base,5)
    if st.session_state.trl_field == "Yes": base = max(base,6)
    if st.session_state.trl_mfg == "Partial": base = max(base,6)
    if st.session_state.trl_mfg == "Yes": base = max(base,7)
    return base
if st.button("Estimate TRL"):
    trl = estimate_trl()
    st.session_state["trl_level"] = trl
    st.success(f"Estimated TRL: **{trl}**")
