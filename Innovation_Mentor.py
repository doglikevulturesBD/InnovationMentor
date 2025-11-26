import streamlit as st

st.set_page_config(
    page_title="Innovation Mentor Platform",
    layout="wide",
    page_icon="💡"
)

# ---------------------------
# CUSTOM STYLES
# ---------------------------
st.markdown("""
<style>
.big-title {
    font-size: 46px !important;
    font-weight: 800 !important;
    margin-bottom: 5px;
}
.subtitle {
    font-size: 19px !important;
    color: #555;
    margin-bottom: 25px;
}
.section-header {
    font-size: 26px !important;
    font-weight: 700 !important;
    margin-top: 25px;
}
.body-text {
    font-size: 17px !important;
    color: #444;
    line-height: 1.6;
}
.footer {
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #dddddd;
    color: #666;
    font-size: 13px;
}
.footer a {
    color: #0073e6;
    text-decoration: none;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------
# HEADER
# ---------------------------
st.markdown('<div class="big-title">Innovation Mentor Platform</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">A lightweight, structured, and evolving support tool to help innovators strengthen proposals and navigate commercialisation.</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------------------
# ABOUT THE PLATFORM
# ---------------------------
st.markdown('<div class="section-header">About This Platform</div>', unsafe_allow_html=True)

st.markdown("""
<div class="body-text">
The Innovation Mentor Platform is designed to help innovators, entrepreneurs, researchers, and portfolio managers think more clearly and make better decisions.
It provides structured guidance across the core areas required for strong innovation proposals and early-stage commercialisation.

This is an evolving tool, currently in **MVP testing**, and features will continue to improve over time.
</div>
""", unsafe_allow_html=True)

# ---------------------------
# MODULE EXPLANATIONS
# ---------------------------
st.markdown('<div class="section-header">What Each Module Does</div>', unsafe_allow_html=True)

st.markdown("""
### TRL Assessment  
A structured tool to help you identify your correct Technology Readiness Level (TRL) based on international TRL definitions.  
It ensures proposers and evaluators speak the same language about technical maturity.

### Business Model Selector  
A guided journey that analyses your innovation and identifies the best-aligned business models.  
Using structured logic and data, it evaluates over 70 business model patterns to help shape your route to market.

### Financial Projections  
Simple, early-stage financial thinking. Helps you explore revenue potential, basic cost structures, and realistic growth scenarios.

### IP Management  
A place to record your intellectual property foundations, improvements, protection strategies, and novelty claims.

### Commercialisation Strategy  
Helps you define your target market, value proposition, pricing approach, distribution channels, and competitive logic.

### Risk Dashboard  
Structured analysis of technical, operational, financial, and market risks — and possible mitigation strategies.

---

These modules are meant to support clarity and improve the quality of proposals and innovation decisions.
They are not a final authority, but a **thinking partner** in your innovation journey.
""")

st.markdown("---")

# ---------------------------
# MVP NOTE
# ---------------------------
st.markdown('<div class="section-header">MVP Status</div>', unsafe_allow_html=True)

st.markdown("""
<div class="body-text">
This platform is currently operating as an **MVP (Minimum Viable Product)**.
Features, scoring logic, and guidance systems will be enhanced in future iterations as real-world usage data,
user feedback, and validation insights are incorporated.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------------------
# LEGAL DISCLAIMER
# ---------------------------
st.markdown("""
<div class="footer">
<b>Disclaimer:</b><br>
This platform provides structured guidance only. It is not a substitute for legal, financial, regulatory, or IP advice.
All decisions made using this platform remain the responsibility of the user.
Refer to the <a href="./Legal_and_Compliance">Legal & Compliance Section</a> for full details.
</div>
""", unsafe_allow_html=True)
