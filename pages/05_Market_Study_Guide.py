import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import streamlit as st
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("🔒 Please log in first.")
    st.stop()

if st.session_state.role == "Demo":
    st.warning("🚫 This section is not available in demo mode.")
    st.stop()


st.set_page_config(page_title="Market Study Guide", layout="wide")
st.title("🌍 Market Study Guide (Compact Dashboard Edition)")

st.markdown("""
This guided worksheet helps you define and validate your **market** before finalizing your financials.  
Each section contributes to an overall **Market Readiness Score**, which can be exported or compared against financial readiness.
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

# --- Smaller TAM–SAM–SOM pyramid ---
st.subheader("Market Size Visualisation (TAM–SAM–SOM Pyramid)")
fig, ax = plt.subplots(figsize=(2.5, 2.5))
ax.barh(["TAM", "SAM", "SOM"], [tam, sam, som], color=["#c7d6f9", "#89b4f8", "#4178e0"])
ax.set_xlabel("Market Size (R)", fontsize=8)
ax.tick_params(axis="y", labelsize=8)
ax.tick_params(axis="x", labelsize=8)
ax.invert_yaxis()
ax.grid(axis="x", linestyle="--", alpha=0.4)
for i, v in enumerate([tam, sam, som]):
    ax.text(v, i, f"R{v/1_000_000:.1f}M", va="center", ha="left", fontsize=7)
st.pyplot(fig, use_container_width=False, width=300)

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
# 6️⃣ Market Readiness Score
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

# ----------------------------
# 7️⃣ Comparison with Financial Readiness
# ----------------------------
st.header("7. Market vs Financial Readiness")

financial_readiness = st.slider("Estimate your Financial Readiness (%)", 0, 100, 70)

fig2, ax2 = plt.subplots(figsize=(2.5, 2.5))
ax2.bar(["Market", "Financial"], [score, financial_readiness], color=["#4a90e2", "#f5a623"], width=0.5)
ax2.set_ylim(0, 100)
ax2.set_ylabel("Readiness (%)", fontsize=8)
ax2.set_title("Market vs Financial Readiness", fontsize=9)
ax2.tick_params(axis="x", labelsize=8)
for i, v in enumerate([score, financial_readiness]):
    ax2.text(i, v + 2, f"{v:.0f}%", ha="center", va="bottom", fontsize=8)
st.pyplot(fig2, use_container_width=False, width=300)

with st.expander("💡 Mentor Insight"):
    if score < financial_readiness - 10:
        st.info("Your financial model is ahead of your market validation — gather more customer or competitor data.")
    elif financial_readiness < score - 10:
        st.info("Your market validation is strong — focus on improving financial projections and funding strategy.")
    else:
        st.success("Balanced progress between market validation and financial planning.")

# ----------------------------
# 8️⃣ Export Summary
# ----------------------------
st.header("8. Export Summary")

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
Financial Readiness: {financial_readiness}%
"""

st.download_button(
    "⬇️ Download Market Study Summary",
    data=summary.encode("utf-8"),
    file_name="market_study_summary.txt",
    mime="text/plain",
    use_container_width=True
)
