import streamlit as st

st.header("📖 Innovation Glossary")
st.markdown("Browse or search key terms used across this app.")

# Expanded glossary (about 20 starter terms)
glossary = {
    "Accelerator": "A short-term, intensive program that supports early-stage startups with mentorship, resources, and sometimes funding.",
    "Business Model": "How a company creates, delivers, and captures value — describing its customers, value proposition, and revenue streams.",
    "Business Plan": "A formal document outlining a business’s goals, strategies, target market, and financial projections.",
    "Commercialisation": "The process of bringing a product or service to market, including production, sales, and distribution.",
    "Design Thinking": "A problem-solving approach focused on understanding user needs, ideation, prototyping, and iterative testing.",
    "Disruptive Innovation": "A new product or service that creates a new market and displaces existing market leaders.",
    "Entrepreneurship": "The process of designing, launching, and running a new business, often involving risk and innovation.",
    "Freemium Model": "A pricing strategy where basic services are free, but advanced features require payment.",
    "Go-to-Market Strategy": "A plan for launching a product, defining target customers, channels, pricing, and marketing tactics.",
    "Incubator": "An organisation or program that provides early-stage startups with resources, mentorship, and office space to grow.",
    "Innovation Management": "The discipline of managing processes that generate and implement new ideas, products, or services.",
    "Intellectual Property (IP)": "Legal rights that protect innovations, including patents, trademarks, copyrights, and trade secrets.",
    "Market Validation": "Gathering evidence that customers want and will pay for your product or service.",
    "Minimum Viable Product (MVP)": "A simplified version of a product built to test a business idea with minimal resources.",
    "Pitch Deck": "A short presentation used to communicate a business idea to investors, partners, or other stakeholders.",
    "Pilot Project": "A small-scale initial study to evaluate feasibility, time, cost, and risk before a full-scale rollout.",
    "Return on Investment (ROI)": "A measure of profitability calculated as (gain from investment - cost) / cost.",
    "Stakeholders": "Individuals or groups with an interest or stake in the success of a project or business.",
    "Technology Readiness Level (TRL)": "A 1–9 scale indicating how mature a technology is, from basic concept (TRL 1) to fully commercial (TRL 9).",
    "Value Proposition": "The unique benefits and value a product or service offers to its target customers.",
    "IRR (Internal Rate of Return)": "The average annual rate of return earned on an investment, based on its cashflows. It represents the discount rate at which NPV = 0.",
    "NPV (Net Present Value)": "The value of future cashflows in today's money, after discounting by the cost of capital. A positive NPV means the project is expected to create value.",
    "ROI (Return on Investment)": "A simple profitability measure: (Gain - Cost) / Cost, showing how much profit is earned for every rand invested.",
    "LCOE (Levelised Cost of Energy)": "The average cost per kWh of energy produced by a system over its lifetime, useful for comparing energy projects."

}

# Sort glossary alphabetically
sorted_terms = dict(sorted(glossary.items(), key=lambda x: x[0].lower()))

# Search box
query = st.text_input("🔍 Search a term")

# Display filtered and sorted results
for term, definition in sorted_terms.items():
    if query.strip() == "" or query.lower() in term.lower() or query.lower() in definition.lower():
        st.markdown(f"### {term}")
        st.write(definition)
        st.divider()
