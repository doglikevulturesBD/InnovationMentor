import streamlit as st
import pandas as pd
import qrcode
from PIL import Image

st.header("📖 Innovation Mentor Glossary")
st.markdown("Browse, search, and share key innovation terms.")

# ========================
# Load Glossary
# ========================
@st.cache_data
def load_glossary():
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
for _, row in filtered.sort_values("term").iterrows():
    with st.expander(row["term"]):
        st.write(row["definition"])

# ========================
# QR Code
# ========================
st.markdown("---")
st.subheader("📱 Share this Glossary")

# Replace with your deployed Streamlit app URL
glossary_url = "https://compendiumofacuriosmind.streamlit.app/Innovation_Mentor"

if st.button("Generate QR Code"):
    qr = qrcode.QRCode(version=1, box_size=8, border=4)
    qr.add_data(glossary_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    st.image(img, caption="Scan to open Innovation Mentor Glossary", use_container_width=False)

