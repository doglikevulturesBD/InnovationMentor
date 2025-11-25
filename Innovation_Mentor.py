import streamlit as st

st.set_page_config(page_title="Innovation Mentor", layout="wide")

st.title("Innovation Mentor")
st.markdown("Your digital guide through the innovation and commercialisation journey.")

st.markdown("---")

st.markdown("### Quick Access Modules")

st.markdown("""
- [TRL Assessment](./01_TRL_Assessment)
- [Business Model Selector](./02_Business_Model)
- [Financial Projections](./03_Financial_Projection)
- [IP Management & Protection](./04_IP_Management)
- [Commercialisation Strategy Builder](./05_Commercialisation_Strategy)
- [Market Study Guide](./07_Market_Study)
- [Financing Options Explorer](./08_Financing_Options)
- [Export Report (Coming Soon)](./09_Export_Report)
- [Risk Dashboard (Coming Soon)](./06_Risk_Dashboard)
""")

st.markdown("---")

st.markdown("### About This Platform")
st.markdown("""
The **Innovation Mentor** is an integrated digital toolkit designed to help innovators, founders, researchers, and project teams navigate the complex journey from idea to market.  
This platform brings together industry best practices, commercialisation frameworks, and practical tools used in real-world project evaluation.

Below is a quick overview of what each section offers:

#### TRL Calculator  
Determine your Technology Readiness Level with a guided assessment based on international TRL frameworks. Get a clear view of your development stage and what is required to advance.

#### Business Model Selector  
Choose the most suitable business model for your innovation. Includes templates, examples, and guiding questions.

#### Financial Projections  
A starter tool to help you build simple, logic-driven revenue, cost, and cashflow projections. Ideal for early-stage financial planning.

#### Market Study Guide  
A structured approach to understanding your market size, customers, competitors, and value proposition.

#### Commercialisation Strategy Builder  
Define your route to market, identify partners, outline activities, and map out your deployment and scaling pathways.

#### IP Management & Selection  
Guidance on protecting your intellectual property, including patents, trademarks, copyrights, and trade secrets — with decision support.

#### Financing Options Explorer  
Discover suitable funding pathways including grants, venture capital, impact funding, government support, and blended finance.

#### Export Report *(Coming Soon)*  
Export your full innovation report as a PDF or structured document.

#### Risk Dashboard *(Coming Soon)*  
An integrated risk view covering technical, commercial, financial, operational, and regulatory risks.

---

### MVP Notice  
This is an early release of the Innovation Mentor platform.  
Some sections are still under development and will be added over time.  
Your feedback is welcome and helps shape future updates.
""")


st.markdown("---")

# Disclaimer + License Section
st.markdown("### Disclaimer & Licence")

st.info("""
**Prototype Version — Independent Project**

st.caption(
    "This platform uses temporary session cookies strictly for navigation and tool functionality. "
    "No tracking, analytics, or personal identifiers are stored."
)


st.markdown("### Innovator Integrity Pledge")
st.info("""
By using the Innovation Mentor platform, you affirm that you will:
- engage honestly with each tool and reflection prompt,
- use the platform ethically and in good faith,
- maintain respect for intellectual property and the innovation journey,
- avoid misrepresentation of results, assessments, or commercial potential,
- and commit to learning, growth, and responsible innovation.
""")


st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: grey; font-size: 13px;'>"
    "Innovation Mentor – MVP Version • Created by Brandon Davoren<br>"
    "<a href='./10_Legal_and_Compliance' style='color: grey;'>Legal & Compliance</a> • "
    "<a href='./10_Legal_and_Compliance' style='color: grey;'>Privacy</a> • "
    "Session cookies only for functionality, no tracking."
    "</div>",
    unsafe_allow_html=True
)

