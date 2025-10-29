import streamlit as st
import pandas as pd
import io
from datetime import datetime

st.set_page_config(page_title="Market Study Guide", layout="wide")
st.title("🌍 Market Study Guide (Phase 1)")

st.markdown("""
This guided worksheet helps you define and validate your **market** before finalizing your financials.  
Each section contributes to an overall **Market Readiness Score**, which you can export for funding applications.
""")

# ----------------------------
# 1️⃣ Market Definition
# ----------------------------
st.header("1. Market Definition")

col1, col2 = st.columns(2)
with col1:
    industry = st.text_input("Industry / Sector", "Energy & Mobility")
    geography = st.text_input("Primary Market Geography", "South Africa")
with col2:
    target_customer = st.text_input("Primary Customer Type", "Municipal fleet operators")
    product_type = st.selectbox("Offering Type", ["Product", "Service", "Platform", "Hybrid"], index=0)

market_problem = st.text_area(
    "What problem are you solving, and why does it matter?",
    "Example: Rising fuel costs and emissions in municipal fleets."
)

# ----------------------------
# 2️⃣ Market Size & Growth
# ----------------------------
st.header("2. Market Size & Growth")

col1, col2, col3 = st.columns(3)
with col1:
    tam = st.number_input("Total Addressable Market (TAM, R)", 0, 1_000_000_000_000, 10_000_000, step=100_000)
with col2:
    sam = st.number_input("Serviceable Available Market (SAM, R)", 0, 1_000_000_000_000, 5_000_000, step=100_000)
with col3:
    som = st.number_input("Serviceable Obtainable Market (SOM, R)", 0, 1_000_000_000_000, 1_000_000, step=50_000)

growth_rate = st.slider("Expected Annual Market Growth (%)", 0.0, 0.3, 0.08, step=0.01)

# ----------------------------
# 3️⃣ Competition Mapping
# ----------------------------
st.header("3. Competition Mapping")

st.caption("List your top competitors or substitutes and how you differentiate.")
default_comp_df = pd.DataFrame({
    "Competitor / Substitute": ["ExampleCo", "LocalAlt", "DIY Methods"],
    "Price Range (R)": ["10000–15000", "7000–9000", "n/a"],
    "Key Strength": ["Brand trust", "Low cost", "Accessibility"],
    "Your Advantage": ["Higher efficiency", "Better support", "Technology"]
})
comp_df = st.data_editor(default_comp_df, use_container_width=True, num_rows="dynamic")

# ----------------------------
# 4️⃣ Customer Validation
# ----------------------------
st.header("4. Customer Validation")

col1, col2 = st.columns(2)
with col1:
    spoke_customers = st.radio("Have you spoken to potential customers?", ["Yes", "No"], index=0)
    num_interviews = st.number_input("How many customer interviews / surveys completed?", 0, 500, 10)
with col2:
    pilot_done = st.radio("Have you done any pilots or demos?", ["Yes", "No"], index=1)
    pilot_feedback = st.slider("Average customer interest (1–5)", 1, 5, 4)

# ----------------------------
# 5️⃣ Go-to-Market Strategy
# ----------------------------
st.header("5. Go-to-Market Strategy")

channels = st.multiselect(
    "Which channels will you use to reach customers?",
    ["Direct sales", "Distributors / partners", "Online / e-commerce", "Tenders / procurement", "Franchise / licensing"]
)
pricing_strategy = st.selectbox(
    "Pricing approach",
    ["Cost-plus", "Market-based", "Value-based", "Tiered / subscription"]
)
marketing_readiness = st.slider("How ready is your marketing / branding? (%)", 0, 100, 60)

# ----------------------------
# 6️⃣ Readiness Scoring
# ----------------------------
st.header("6. Market Readiness Score")

score = 0
if spoke_customers == "Yes": score += 15
score += min(num_interviews * 1.5, 15)
if pilot_done == "Yes": score += 15
score += (pilot_feedback - 1) * 5
score += min(len(channels) * 5, 15)
score += (marketing_readiness / 10)
score += (growth_rate * 100) / 3

score = min(round(score, 1), 100)
readiness_label = (
    "🔴 Early (Below 50%)" if score < 50 else
    "🟡 Developing (50–75%)" if score < 75 else
    "🟢 Ready (Above 75%)"
)

st.metric("Market Readiness", f"{score} %", readiness_label)

with st.expander("💡 Mentor Insight"):
    if score < 50:
        st.info("Focus on customer discovery — validate the problem and price points before scaling.")
    elif score < 75:
        st.info("Good foundation — gather more pilot data and refine your channel strategy.")
    else:
        st.success("Strong market validation — ready to support financial and funding applications.")

# ----------------------------
# 7️⃣ Export Summary
# ----------------------------
st.header("7. Export Summary")

summary = f"""
Market Study Summary — {datetime.now().strftime("%Y-%m-%d %H:%M")}

Industry: {industry}
Geography: {geography}
Customer: {target_customer}
Offering Type: {product_type}

Problem Statement:
{market_problem}

TAM: R{tam:,.0f} | SAM: R{sam:,.0f} | SOM: R{som:,.0f}
Growth Rate: {growth_rate*100:.1f}%

Customer Engagement:
Spoken to customers: {spoke_customers}
Interviews: {num_interviews}
Pilot done: {pilot_done}
Average interest: {pilot_feedback}/5

Go-to-Market:
Channels: {", ".join(channels) if channels else "—"}
Pricing Strategy: {pricing_strategy}
Marketing Readiness: {marketing_readiness}%

Market Readiness Score: {score}% ({readiness_label})
"""

st.download_button(
    "⬇️ Download Market Study Summary",
    data=summary.encode("utf-8"),
    file_name="market_study_summary.txt",
    mime="text/plain",
    use_container_width=True
)
