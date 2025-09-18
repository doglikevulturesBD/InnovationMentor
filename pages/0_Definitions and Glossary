import streamlit as st

st.header("📖 Innovation Glossary")
st.markdown("Browse or search key terms used across this app.")

# Dictionary of terms
glossary = {
    "TRL (Technology Readiness Level)": "A 1–9 scale indicating how mature a technology is, from basic concept (TRL 1) to fully commercial (TRL 9).",
    "IP (Intellectual Property)": "Legal rights that protect innovations, including patents, trademarks, copyrights, and trade secrets.",
    "Commercialisation": "The process of taking a product or service to market, including production, sales, and distribution.",
    "Business Model": "How a company creates, delivers, and captures value — describing its customers, value proposition, and revenue streams.",
    "Pilot Project": "A small-scale initial study to evaluate feasibility, time, cost, and risk before a full-scale rollout.",
    "Market Validation": "Gathering evidence that customers want and will pay for your product or service."
}

# Search box
query = st.text_input("🔍 Search a term")

for term, definition in glossary.items():
    if query.strip() == "" or query.lower() in term.lower() or query.lower() in definition.lower():
        st.markdown(f"### {term}")
        st.write(definition)
        st.divider()
