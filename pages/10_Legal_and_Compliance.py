import streamlit as st

st.set_page_config(page_title="Legal & Compliance", layout="wide")

st.title("Legal & Compliance")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "Terms of Use", 
    "Licence Summary", 
    "Privacy & POPIA Notice", 
    "POPIA Compliance Memo"
])

# -------------------------
# 1. TERMS OF USE
# -------------------------
with tab1:
    st.header("Terms of Use")
    st.markdown("""
These Terms of Use govern your access to and use of the **Innovation Mentor** platform.

### 1. Purpose of the Platform
The platform is designed as a personal, independent educational tool to assist innovators, founders, and learners in navigating the innovation and commercialisation journey.

It is **not affiliated with**, **endorsed by**, or **representing** any organisation, agency, or employer.

### 2. No Professional or Official Advice
All content is provided for general guidance and educational purposes only.  
It does not constitute:
- legal advice  
- financial advice  
- funding guidance  
- engineering guidance  
- commercialisation decisions  
- IP or patent advice  

The platform must **not** be used for:
- official evaluations  
- grant/investment decisions  
- due diligence  
- internal or external organisational assessment  

Decisions made based on the platform are solely your responsibility.

### 3. Acceptable Use
By using the platform, you agree that you will not:
- misuse or attempt to reverse-engineer the tool  
- use it for unlawful, harmful, or misleading purposes  
- impersonate others or provide false information  
- upload harmful content or malicious code  
- bypass required reflection checkpoints  

### 4. Intellectual Property
All structured logic, frameworks, worksheet templates, workflows, and content remain the property of the creator unless otherwise stated.

### 5. Data Handling
Use of the platform implies agreement with the Privacy and POPIA Notice.

### 6. Liability Limitation
The creator is not liable for:
- business losses  
- grant/funding decisions  
- project outcomes  
- misunderstandings or misinterpretations  
- indirect, incidental, or consequential damages  

### 7. Updates to These Terms
These Terms may be updated as the platform grows. Continued use constitutes acceptance of updated terms.

© 2025 Innovation Mentor Platform — Educational use only.
""")


# -------------------------
# 2. LICENCE SUMMARY
# -------------------------
with tab2:
    st.header("Licence Summary")
    st.markdown("""
The **Innovation Mentor** platform, including its logic, templates, and content, is released under:

## **Creative Commons Attribution–NonCommercial 4.0 International (CC BY–NC 4.0)**

You may:
- share the content  
- adapt the templates  
- build upon the logic  
- remix educational materials  

**As long as:**
- attribution is clear and visible  
- usage is strictly **non-commercial**  

You may **not**:
- resell the tool  
- incorporate it into commercial products  
- charge for access  
- represent it as your own proprietary system  

To request commercial permissions or collaboration, please contact the creator directly.
""")


# -------------------------
# 3. PRIVACY & POPIA NOTICE
# -------------------------
with tab3:
    st.header("Privacy & POPIA Notice")
    st.markdown("""
This platform adheres to the **data minimisation** and **purpose limitation** principles of the Protection of Personal Information Act (POPIA).

### What Data is Collected
- Anonymous reflections (private, admin-only)  
- Optional public comments (user-controlled)  
- Non-identifying usage counts (module visits)

No personal identifiers are collected, including:
- names  
- email addresses  
- ID numbers  
- IP addresses  
- device information  

The MVP implements **no cookies**, **no tracking**, **no analytics**, and **no background monitoring**.

### Why Data is Collected
To support:
- reflection-based learning  
- personal insight  
- improvement of educational tools  
- understanding module effectiveness  

### Data Storage
Data is stored locally in:
- **reflections.json** (private reflections)  
- **comments.json** (optional public comments)  

All data remains local to your device unless you explicitly export or save it.

These files are never shared with third parties.

### User Rights
Because no personal data is stored, POPIA rights relating to personal information do not apply.  
Users may request deletion of their reflections or comments if needed.

### Security
The platform is designed to prevent:
- identity inference  
- behavioural profiling  
- personal data leakage  

Future updates may include encryption for added protection.
""")


# -------------------------
# 4. POPIA COMPLIANCE MEMO
# -------------------------
with tab4:
    st.header("POPIA Compliance Memo")
    st.markdown("""
This memo outlines how the **Innovation Mentor** MVP aligns with POPIA and standard data protection principles.

### 1. Minimal Data Collection
Only anonymous, non-personal behavioural data is captured.  
No personal information is collected or required for platform functionality.

### 2. Purpose Limitation
Data is collected solely to:
- enable reflection gating  
- support learning  
- improve tool effectiveness  

No secondary or commercial use exists.

### 3. Storage & Safeguards
Reflections and comments are stored in isolated JSON files, not linked to any personal identity.  
There is no risk of re-identification because no identifiers are ever stored.

### 4. User Transparency
Users are clearly informed of:
- what data is collected  
- why it is collected  
- how it is used  
- their rights  

This meets POPIA Section 18 transparency requirements.

### 5. Data Quality & Access
Data is:
- anonymous  
- low-risk  
- not cross-linked  
- not shared externally  

### 6. Risk Assessment
Because no personally identifiable information is collected, this platform falls within POPIA’s **low-risk category**.

### 7. Compliance Confirmation
As an educational MVP, the tool meets all relevant POPIA requirements under:
- Purpose Limitation  
- Data Minimisation  
- Collection Limitation  
- Security Safeguards  
- Openness  

This memo may evolve as the platform grows into a multi-user system.
""")

