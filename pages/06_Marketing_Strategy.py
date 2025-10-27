
import streamlit as st
st.title("Marketing Strategy (MVP)")
segment = st.text_input("Primary customer segment", "Fleet operators / SMEs")
value_prop = st.text_area("Value proposition (1–2 sentences)", "Cut fuel costs by 25% with a pay-per-use EV charging bundle.")
pricing = st.text_input("Pricing approach", "Subscription + usage")
channels = st.text_area("Channels", "Direct sales; partner resellers; pilot with 3 early adopters")
st.session_state["marketing"] = {"segment": segment, "value_prop": value_prop, "pricing": pricing, "channels": channels}
