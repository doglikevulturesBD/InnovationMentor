import streamlit as st

st.set_page_config(page_title="Feedback", layout="wide")

# -------------------------------
# HEADER
# -------------------------------
st.markdown("""
<h1 style='text-align:center; margin-bottom:0;'>💬 Feedback & Suggestions</h1>
<p style='text-align:center; color:#555; font-size:17px;'>
Your input helps shape the Innovation Mentor Platform.  
This MVP is evolving, and your feedback determines what we build next.
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# -------------------------------
# EMBED GOOGLE FORM
# -------------------------------
st.subheader("📝 Full Feedback Form")

st.markdown("Please complete the detailed form below:")

st.components.v1.html(
    '''
    <iframe src="https://docs.google.com/forms/d/e/1FAIpQLSc61A8kolpNa1NxKwR1eoYF7MLSwp-rofJTOS9XSaw30fwnWg/viewform?embedded=true"
    width="100%" height="1800" frameborder="0" marginheight="0" marginwidth="0">
    Loading…
    </iframe>
    ''',
    height=1850,
    scrolling=True
)

st.markdown("---")

# -------------------------------
# FOOTER DISCLAIMER
# -------------------------------
st.markdown("""
<br>
<div style='font-size:12px; color:#777; text-align:center; border-top:1px solid #ddd; padding-top:15px;'>
This platform is an MVP and is under active development.  
Feedback submitted through this form is stored securely by Google Forms/Google Workspace.  
For legal notices, please refer to the Legal section of the platform.
</div>
<br><br>
""", unsafe_allow_html=True)
