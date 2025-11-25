import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Market Study Guide", layout="wide")

# ----------------------------------------------------------
# HEADER
# ----------------------------------------------------------
st.title("📊 Market Study Guide")
st.caption("A compact, structured worksheet to validate your market before finalising commercialisation and funding plans.")

st.markdown("""
This module helps you build confidence in your **market**, your **customers**, and your **positioning**.  
The output feeds directly into your **Commercialisation Strategy** and **Financial Projections**.
""")

st.markdown("---")

# ----------------------------------------------------------
# 1️⃣ MARKET DEFINITION
# ----------------------------------------------------------
st.header("1. Market Definition")

col1, col2 = st.columns(2)
with col1:
    industry = st.text_input("Industry / Sector", "Energy & Mobility")
    geography = st.text_input("Primary Geography", "South Africa")
with col2:
    target_customer = st.text_input("Primary Customer Type", "Municipal fleet operators")
    product_type = st.selectbox("Offering Type", ["Product", "Service", "Platform", "Hybrid"], index=0)

market_problem = st.text_area(
    "Problem Statement",
    "Example: Rising fuel costs and emissions in municipal fleets."
)

st.markdown("---")

# ----------------------------------------------------------
# 2️⃣ MARKET SIZE & GROWTH
# ----------------------------------------------------------
st.header("2. Market Size & Growth")

col1, col2, col3 = st.columns(3)
with col1:
    tam = st.number_input("TAM — Total Addressable Market (R)", 0, 1_000_000_000_000, 10_000_000, step=100_000)
with col2:
    sam = st.number_input("SAM — Serviceable Available Market (R)", 0, 1_000_000_000_000, 5_000_000, step=100_000)
with col3:
    som = st.number_input("SOM — Serviceable Obtainable Market (R)", 0, 1_000_000_000_000, 1_000_000, step=50_000)

growth_rate = st.slider("Expected Annual Growth (%)", 0.0, 30.0, 8.0, step=0.5) / 100

st.subheader("TAM–SAM–SOM Pyramid (Compact View)")
fig, ax = plt.subplots(figsize=(2.5, 2.5))
ax.barh(["TAM", "SAM", "SOM"], [tam, sam, som], color=["#c7d6f9", "#89b4f8", "#4178e0"])
ax.set_xlabel("Market Size (R)", fontsize=8)
ax.tick_params(axis="y", labelsize=8)
ax.tick_params(axis="x", labelsize=8)
ax.grid(axis="x", linestyle="--", alpha=0.3)
ax.invert_yaxis()
for i, v in enumerate([tam, sam, som]):
    ax.text(v, i, f"R{v/1_000_000:.1f}M", va="center", ha="left", fontsize=7)
st.pyplot(fig, width=300)

st.markdown("---")

# ----------------------------------------------------------
# 3️⃣ COMPETITION MAPPING
# ----------------------------------------------------------
st.header("3. Competition Mapping")
st.caption("Map your competitive landscape and identify your advantages.")

default_comp_df = pd.DataFrame({
    "Competitor / Substitute": ["ExampleCo", "LocalAlt", "DIY Methods"],
    "Price Range (R)": ["10000–15000", "7000–9000", "—"],
    "Key Strength": ["Brand trust", "Low cost", "Convenience"],
    "Your Advantage": ["Higher efficiency", "Better support", "Technology-based"]
})

comp_df = st.data_editor(
    default_comp_df,
    use_container_width=True,
    num_rows="dynamic"
)

st.markdown("---")

# ----------------------------------------------------------
# 4️⃣ CUSTOMER VALIDATION
# ----------------------------------------------------------
st.header("4. Customer Validation")

col1, col2 = st.columns(2)
with col1:
    spoke_customers = st.radio("Have you spoken to potential customers?", ["Yes", "No"], index=0)
    num_interviews = st.number_input("Customer Interviews Completed", 0, 500, 10)
with col2:
    pilot_done = st.radio("Have you run pilots or demos?", ["Yes", "No"], index=1)
    pilot_feedback = st.slider("Avg Customer Interest (1–5)", 1, 5, 4)

st.markdown("---")

# ----------------------------------------------------------
# 5️⃣ GO-TO-MARKET STRATEGY
# ----------------------------------------------------------
st.header("5. Go-to-Market Strategy")

channels = st.multiselect(
    "Planned Channels",
    ["Direct sales", "Distributors / partners", "Online / e-commerce", "Tenders / procurement", "Licensing"],
)

pricing_strategy = st.selectbox(
    "Pricing Strategy",
    ["Cost-plus", "Market-based", "Value-based", "Tiered / subscription"]
)

marketing_readiness = st.slider("Marketing/Branding Readiness (%)", 0, 100, 60)

st.markdown("---")

# ----------------------------------------------------------
# 6️⃣ MARKET READINESS SCORE
# ----------------------------------------------------------
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
    "🔴 Early (<50%)" if score < 50 else
    "🟡 Developing (50–75%)" if score < 75 else
    "🟢 Ready (>75%)"
)

st.metric("Market Readiness Score", f"{score}%", readiness_label)

# Save for later modules
st.session_state["market_readiness"] = score

st.markdown("---")

# ----------------------------------------------------------
# 7️⃣ MARKET VS FINANCIAL READINESS
# ----------------------------------------------------------
st.header("7. Market vs Financial Readiness")

financial_readiness = st.slider("Financial Readiness (%)", 0, 100, 70)

fig2, ax2 = plt.subplots(figsize=(2.5, 2.5))
ax2.bar(["Market", "Financial"], [score, financial_readiness], color=["#4a90e2", "#f5a623"], width=0.5)
ax2.set_ylim(0, 100)
ax2.set_ylabel("Readiness (%)", fontsize=8)
for i, v in enumerate([score, financial_readiness]):
    ax2.text(i, v + 2, f"{v:.0f}%", ha="center", va="bottom", fontsize=8)
st.pyplot(fig2)

with st.expander("💡 Mentor Insight"):
    if score < financial_readiness - 10:
        st.info("Your financial model is running ahead of market validation — strengthen customer discovery.")
    elif financial_readiness < score - 10:
        st.info("Your market validation is strong — refine financials and funding models next.")
    else:
        st.success("Balanced progress between market and financial readiness.")

st.markdown("---")

# ----------------------------------------------------------
# 8️⃣ EXPORT SUMMARY
# ----------------------------------------------------------
st.header("8. Export Summary")

summary = f"""
Market Study Summary — {datetime.now().strftime("%Y-%m-%d %H:%M")}

Industry: {industry}
Geography: {geography}
Customer: {target_customer}
Offering Type: {product_type}

Problem: {market_problem}

TAM: R{tam:,}
SAM: R{sam:,}
SOM: R{som:,}
Growth Rate: {growth_rate*100:.1f}%

Customer Engagement:
- Spoke to customers: {spoke_customers}
- Interviews: {num_interviews}
- Pilot done: {pilot_done}
- Avg interest: {pilot_feedback}/5

Go-to-Market:
- Channels: {", ".join(channels) if channels else "—"}
- Pricing: {pricing_strategy}
- Marketing readiness: {marketing_readiness}%

Market Readiness Score: {score}% ({readiness_label})
Financial Readiness: {financial_readiness}%
"""

st.download_button(
    "⬇️ Download Market Study Summary",
    data=summary.encode("utf-8"),
    file_name="market_study_summary.txt",
    mime="text/plain",
    use_container_width=True
)

