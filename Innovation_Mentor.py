import streamlit as st


st.set_page_config(page_title="Innovation Mentor", page_icon="💡", layout="wide")


st.title("Welcome to the Innovation Mentor Platform")


st.markdown("---")
st.markdown("### Quick Access Links")
if role == "Admin":
    st.markdown("- [TRL Assessment](./01_TRL_Assessment)")
    st.markdown("- [Business Model](./02_Business_Model)")
    st.markdown("- [Financial Projections](./03_Financial_Projection)")
    st.markdown("- [IP Management](./04_IP_Management)")
    st.markdown("- [Commercialisation Strategy](./05_Commercialisation_Strategy)")
    st.markdown("- [Risk Dashboard](./06_Risk_Dashboard)")
elif role == "Evaluator":
    st.markdown("- [TRL Assessment](./01_TRL_Assessment)")
    st.markdown("- [Business Model](./02_Business_Model)")
    st.markdown("- [Commercialisation Strategy](./05_Commercialisation_Strategy)")
    st.markdown("- [Risk Dashboard](./06_Risk_Dashboard)")
elif role == "Demo":
    st.markdown("- [TRL Assessment](./01_TRL_Assessment)")
    st.markdown("- [Business Model](./02_Business_Model)")
    st.markdown("- [Commercialisation Strategy](./05_Commercialisation_Strategy)")
