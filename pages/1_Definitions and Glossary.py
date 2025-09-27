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
    return pd.read_json("innovation_glossary.json")

glossary = load_glossary()

# ========================
# Search (simple partial matching)
# ========================
query = st.text_input("🔍 Search a term").lower().strip()

if query:
    filtered = glossary[
        glossary['term'].str.lower().str.contains(query, na=False) |
        glossary['definition'].str.lower().str.contains(query, na=False)
    ]
else:
    filtered = glossary

# ========================
# Display Results by Alphabet
# ========================
if filtered.empty:
    st.warning("No terms found. Try a different keyword.")
else:
    filtered = filtered.sort_values("term")
    current_letter = ""
    for _, row in filtered.iterrows():
        first_letter = row["term"][0].upper()
        if first_letter != current_letter:
            current_letter = first_letter
            st.markdown(f"## {current_letter}")  # Section header for letter
        with st.expander(row["term"]):
            st.write(row["definition"])

# ========================
# Share Section
# ========================
st.markdown("---")
st.subheader("📱 Share this Glossary")
st.info("To share this glossary, copy the URL from your browser or generate a QR code offline (e.g., in Spyder).")

