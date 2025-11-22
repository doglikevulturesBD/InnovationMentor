import streamlit as st

st.set_page_config(page_title="Innovation Mentor", page_icon="💡", layout="wide")

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

#### 🔬 TRL Calculator  
Determine your Technology Readiness Level with a guided assessment based on international TRL frameworks. Get a clear view of your development stage and what is required to advance.

#### 🧩 Business Model Selector  
Choose the most suitable business model for your innovation. Includes templates, examples, and guiding questions.

#### 📊 Financial Projections  
A starter tool to help you build simple, logic-driven revenue, cost, and cashflow projections. Ideal for early-stage financial planning.

#### 🧠 Market Study Guide  
A structured approach to understanding your market size, customers, competitors, and value proposition.

#### 🧭 Commercialisation Strategy Builder  
Define your route to market, identify partners, outline activities, and map out your deployment and scaling pathways.

#### 🧬 IP Management & Selection  
Guidance on protecting your intellectual property, including patents, trademarks, copyrights, and trade secrets — with decision support.

#### 💸 Financing Options Explorer  
Discover suitable funding pathways including grants, venture capital, impact funding, government support, and blended finance.

#### 📤 Export Report *(Coming Soon)*  
Export your full innovation report as a PDF or structured document.

#### ⚠️ Risk Dashboard *(Coming Soon)*  
An integrated risk view covering technical, commercial, financial, operational, and regulatory risks.

---

### 🚀 MVP Notice  
This is an early release of the Innovation Mentor platform.  
Some sections are still under development and will be added over time.  
Your feedback is welcome and helps shape future updates.
""")


st.markdown("---")

# Disclaimer + License Section
st.markdown("### ⚖️ Disclaimer & Licence")

st.info("""
**Prototype Version — Independent Project**

This platform is an independent personal project created for educational and guidance purposes.  
It is **not affiliated with**, **endorsed by**, or **representing** any organisation, agency, or employer.  
All content is provided on an “as is” basis and should not be interpreted as official advice, funding guidance, or legal opinion.

Use of this tool is voluntary and at your own discretion.
""")

st.markdown("""
### 📄 Licence

Unless otherwise noted, the content, logic frameworks, and structure of this platform are released under the following licence:

**Creative Commons Attribution–NonCommercial 4.0 International (CC BY–NC 4.0)**  
You may share and adapt the material for **non-commercial** purposes, provided attribution is given to the original creator.

Commercial use, resale, or replication of the platform, its logic, or its tools is **not permitted** without written permission.

For permissions or collaboration requests, please contact:  
**[Your Name] – Innovation Mentor Creator**  
""")

