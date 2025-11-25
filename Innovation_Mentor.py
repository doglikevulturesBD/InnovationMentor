import streamlit as st

st.set_page_config(page_title="Innovation Mentor", layout="wide")

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.title("Innovation Mentor")

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
It brings together practical tools aligned with real-world evaluation frameworks used in innovation, funding, and commercialisation.

**Key features include:**

- **TRL Calculator** – Determine your technology readiness level and next steps  
- **Business Model Selector** – Find the most suitable model for your innovation  
- **Financial Projection Builder** – Create early-stage financial outlooks  
- **IP Management Guidance** – Understand protection pathways and strategy  
- **Commercialisation Strategy Builder** – Plan your deployment and scaling roadmap  
- **Market Study Guide** – Analyse your customers, competitors, and market  
- **Financing Options Explorer** – Discover suitable funding routes  

More modules will continue to be added as the platform evolves.
""")

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
        <a href='./Legal_and_Compliance' style='color: grey;'>Legal & Compliance</a>
    </div>
    """,
    unsafe_allow_html=True
)

