import streamlit as st
import pandas as pd

# ========================
# Page Setup
# ========================
st.set_page_config(page_title="Innovation Mentor Glossary", layout="wide")
st.header("📖 Innovation Mentor Glossary")
st.markdown("Browse and search key innovation terms for innovators, entrepreneurs, and mentors.")

# ========================
# Load Glossary
# ========================
@st.cache_data
def load_glossary():
    # Ensure you have "innovation_glossary.json" in your repo
    return pd.read_json("innovation_glossary.json")

glossary = load_glossary()

# ========================
# Search
# ========================
query = st.text_input("🔍 Search a term")

filtered = glossary[
    glossary['term'].str.contains(query, case=False, na=False) |
    glossary['definition'].str.contains(query, case=False, na=False)
]

# ========================
# Display Results
# ========================
if filtered.empty:
    st.warning("No terms found. Try a different search keyword.")
else:
    for _, row in filtered.sort_values("term").iterrows():
        with st.expander(row["term"]):
            st.write(row["definition"])

# ========================
# Share Section
# ========================
st.markdown("---")
st.subheader("📱 Share this Glossary")
st.info("To share this glossary, copy the URL from your browser or generate a QR code offline (e.g., in Spyder).")


