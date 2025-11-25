import streamlit as st

st.set_page_config(page_title="Innovation Mentor", layout="wide")

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.title("🚀 Innovation Mentor")

# Premium italic tagline
st.markdown(
    "<div style='font-size:16px; color: grey; font-style: italic;'>Innovating for Innovators</div>",
    unsafe_allow_html=True
)

st.subheader("Your digital companion for navigating the innovation and commercialisation journey.")

st.markdown("---")

# -------------------------------------------------
# ABOUT SECTION
# -------------------------------------------------

st.markdown("### What This Platform Offers")

st.markdown("""
The **Innovation Mentor** is an integrated, lightweight toolkit designed to help innovators, founders, researchers, 
and project teams move from idea to market with clarity and confidence.

It brings together practical tools aligned with real-world evaluation frameworks used in innovation, 
funding, and commercialisation.
""")

# -------------------------------------------------
# RECOMMENDED JOURNEY FLOW
# -------------------------------------------------

st.markdown("### 🧭 Recommended Journey")

st.markdown("""
Follow the modules **from top to bottom** for the best experience and a complete innovation pathway:

1️⃣ **TRL Assessment** – Understand your readiness level  
2️⃣ **Business Model Selector** – Shape how value is delivered  
3️⃣ **Financial Projections** – Build your early financial logic  
4️⃣ **IP Management** – Identify suitable protection strategies  
5️⃣ **Commercialisation Strategy** – Define your route to market  
6️⃣ **Market Study Guide** – Analyse market fit and context  
7️⃣ **Financing Options** – Explore funding pathways  
""")

st.markdown("---")

# -------------------------------------------------
# MODULE LIST (WITH LINKS)
# -------------------------------------------------

st.markdown("### 📂 Quick Access Modules")
st.markdown("""
- 🚦 [TRL Assessment](./01_TRL_Assessment)
- 🧩 [Business Model Selector](./02_Business_Model)
- 📊 [Financial Projections](./03_Financial_Projection)
- 🔐 [IP Management & Protection](./04_IP_Management)
- 🛠️ [Commercialisation Strategy Builder](./05_Commercialisation_Strategy)
- 📘 [Market Study Guide](./07_Market_Study)
- 💰 [Financing Options Explorer](./08_Financing_Options)
- 📄 [Export Report (Coming Soon)](./09_Export_Report)
- ⚠️ [Risk Dashboard (Coming Soon)](./06_Risk_Dashboard)
""")

# -------------------------------------------------
# MVP NOTICE
# -------------------------------------------------

st.info("**MVP Notice:** This is an early release. Some tools are experimental or under development.")

st.markdown("---")

# -------------------------------------------------
# LEGAL REMINDER
# -------------------------------------------------

st.caption(
    "Before using this platform, please review the Legal & Compliance page for terms, licensing, and POPIA information."
)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: grey; font-size: 13px;'>
        Innovation Mentor – MVP Version • Created by Brandon Davoren<br>
        <a href='./10_Legal_and_Compliance' style='color: grey;'>Legal & Compliance</a>
    </div>
    """,
    unsafe_allow_html=True
)

