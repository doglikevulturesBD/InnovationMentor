import streamlit as st

st.set_page_config(page_title="Financing Options", layout="wide")
st.title("💰 Financing Options (MVP)")

st.markdown("""
Early-stage ventures often rely on **non-dilutive grants** and **conditional support**,  
while later stages unlock **blended finance**, **concessional debt**, and **commercial investment**.

This tool gives **simple stage-based suggestions**, not financial advice.
---
""")

# ---- Stage selector ----
stage = st.selectbox(
    "Select your current stage:",
    ["Ideation", "Prototype / TRL 3–5", "Pilot / TRL 6–7", "Commercialisation / TRL 8–9", "Scaling / Growth"]
)

# ---- Recommendations ----
st.subheader("Recommended Financing Options")

if stage == "Ideation":
    st.markdown("""
    - **Small / micro grants**  
    - **Research grants / innovation challenges**  
    - **University or government seed support**  
    - **Founder-funded (low burn)**  
    """)

elif stage == "Prototype / TRL 3–5":
    st.markdown("""
    - **Proof-of-concept grants**  
    - **Conditional grants tied to milestones**  
    - **Early blended finance (grant + loan/light equity)**  
    - **Incubator / accelerator micro-funding**  
    """)

elif stage == "Pilot / TRL 6–7":
    st.markdown("""
    - **Pilot demonstration grants**  
    - **Concessional loans**  
    - **Early-stage venture capital (sector specific)**  
    - **Corporate partnerships / co-development funding**  
    """)

elif stage == "Commercialisation / TRL 8–9":
    st.markdown("""
    - **Revenue-based finance**  
    - **Convertible notes / early equity**  
    - **Project finance (if infrastructure-based)**  
    - **Commercial venture funds**  
    """)

elif stage == "Scaling / Growth":
    st.markdown("""
    - **Private equity / strategic investors**  
    - **Development finance institutions (DFIs)**  
    - **Blended finance structures**  
    - **Long-term concessionary loans (if infrastructure)**  
    """)

st.markdown("---")

# ---- Reflection box ----
st.subheader("📝 Reflection")
st.text_area(
    "How does this influence your financing strategy?",
    height=150,
    key="finance_reflection"
)
