import streamlit as st

st.set_page_config(page_title="Innovation Mentor", layout="wide")

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.title("🚀 Innovation Mentor")
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
# LEGAL + LICENCE
# -------------------------------------------------

st.markdown("### Disclaimer & Licence")

st.info("""
**Prototype Version — Independent Project**

This platform is an independent personal project created for educational and guidance purposes.  
It is **not affiliated with**, **endorsed by**, or **representing** any organisation, agency, or employer.
""")

st.markdown("""
The content, frameworks, and tool structure are released under:

**Creative Commons Attribution–NonCommercial 4.0 (CC BY–NC 4.0)**  
You may share and adapt the material for **non-commercial purposes** with attribution.

Commercial use or replication requires written permission.
""")

# -------------------------------------------------
# COOKIE / SESSION NOTICE
# -------------------------------------------------

st.caption(
    "This platform uses temporary session cookies strictly for navigation and functionality. "
    "No tracking, analytics, or personal identifiers are stored."
)

# -------------------------------------------------
# INTEGRITY PLEDGE
# -------------------------------------------------

st.markdown("### Innovator Integrity Pledge")
st.info("""
By using the Innovation Mentor platform, you agree to:
- engage honestly with reflection prompts,
- use the platform ethically and in good faith,
- respect intellectual property and innovation integrity,
- avoid misrepresentation of assessments or results,
- and commit to responsible, sustainable innovation.
""")

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: grey; font-size: 13px;'>
    Innovation Mentor – MVP Version • Created by Brandon Davoren<br>
    <a href='./10_Legal_and_Compliance' style='color: grey;'>Legal & Compliance</a> • 
    Session cookies only for functionality.
    </div>
    """,
    unsafe_allow_html=True
)


