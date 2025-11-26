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
    font-size: 48px !important;
    font-weight: 800 !important;
    padding-top: 5px;
    margin-bottom: 0px;
}
.subtitle {
    font-size: 20px !important;
    color: #4f4f4f;
    margin-top: 5px;
    margin-bottom: 30px;
}
.section-header {
    font-size: 28px !important;
    font-weight: 700 !important;
    margin-top: 30px;
    margin-bottom: 15px;
}
.card {
    padding: 22px;
    background-color: #f7f9fc;
    border: 1px solid #dfe3e6;
    border-radius: 12px;
    height: 210px;
    transition: all 0.2s ease-in-out;
}
.card:hover {
    background-color: #eef2f5;
    border-color: #cfd5da;
}
.card h3 {
    margin-top: 0px;
    font-weight: 700;
}
.card p {
    color: #555;
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
st.markdown('<div class="subtitle">A guided system for innovators, startups, and evaluators — helping structure proposals, sharpen thinking, and strengthen commercialisation pathways.</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------------------------
# QUICK ACCESS MODULES
# ---------------------------
st.markdown('<div class="section-header">Core Modules</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>TRL Assessment</h3>
        <p>Determine your Technology Readiness Level accurately across all nine stages.</p>
        <a href="./01_TRL_Assessment">Open →</a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>Business Model Selector</h3>
        <p>Evaluate 70+ business models and discover the best fit for your innovation.</p>
        <a href="./02_Business_Model">Open →</a>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3>Financial Projections</h3>
        <p>Explore scenarios, revenue models, cost structures, and your commercial runway.</p>
        <a href="./03_Financial_Projection">Open →</a>
    </div>
    """, unsafe_allow_html=True)


col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="card">
        <h3>IP Management</h3>
        <p>Document novel components, protectable elements, and IP improvement history.</p>
        <a href="./04_IP_Management">Open →</a>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="card">
        <h3>Commercialisation Strategy</h3>
        <p>Define your value proposition, target markets, pricing logic, and pathways.</p>
        <a href="./05_Commercialisation_Strategy">Open →</a>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="card">
        <h3>Risk Dashboard</h3>
        <p>Identify technical, financial, operational, and market risks early.</p>
        <a href="./06_Risk_Dashboard">Open →</a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------
# ABOUT SECTION
# ---------------------------
st.markdown('<div class="section-header">About This Platform</div>', unsafe_allow_html=True)

st.write("""
The Innovation Mentor is built to support innovators, startups, researchers, and evaluators by offering a clean, structured approach to:

- Technology readiness
- Business model alignment
- Commercialisation strategy
- Financial projections
- Risk identification
- Intellectual property thinking

It reduces uncertainty, improves clarity, and helps transform technical ideas into investable opportunities.
""")

st.markdown("---")

# ---------------------------
# LEGAL DISCLAIMER SECTION
# ---------------------------
st.markdown("""
<div class="footer">
<b>Disclaimer:</b><br>
This tool provides guidance to support innovators but does not replace expert legal, financial, IP, or regulatory advice. 
All decisions based on the outputs of this platform remain the responsibility of the user. 
Please refer to the <a href="./Legal_Section">Legal & Compliance Section</a> for full details.
</div>
""", unsafe_allow_html=True)

