
import streamlit as st
from utils.scoring import load_models, trl_gate, score_models

st.title("Business Model Selector (MVP)")

trl = st.session_state.get("trl_level", 4)
st.info(f"Current TRL: **{trl}**")

col1, col2, col3 = st.columns(3)
with col1:
    wants_recurring = st.toggle("Prefer recurring revenue", value=True)
with col2:
    customer_type = st.selectbox("Primary customer type", ["SME","enterprise","government"], index=1)
with col3:
    capex = st.selectbox("Capex reality", ["low","med","high"], index=0)
partner_ready = st.toggle("Have a strong partner/channel?", value=False)

profile = {
    "wants_recurring": wants_recurring,
    "customer_type": customer_type,
    "capex": capex,
    "partner_ready": partner_ready,
}

models = trl_gate(load_models(), trl)
top3 = score_models(profile, models)

st.subheader("Top 3 Recommendations")
for i, item in enumerate(top3, start=1):
    m = item["model"]
    st.markdown(f"**{i}. {m['name']}** — Score: {item['score']}")
    with st.expander("Details"):
        st.write(m["description"])

st.session_state["top3_models"] = [t["model"]["name"] for t in top3]
st.session_state["selected_model"] = st.selectbox("Choose one for finance/roadmap", [t["model"]["name"] for t in top3] if top3 else [])
