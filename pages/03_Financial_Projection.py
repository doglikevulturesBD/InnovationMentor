import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Financial Projection Sandbox", layout="wide")
st.title("💰 Financial Projection Sandbox (Phase 1.5)")

# --- Sidebar Inputs ---
st.sidebar.header("Input Parameters")
years = st.sidebar.slider("Projection Period (years)", 1, 15, 10)
capex = st.sidebar.number_input("Initial CAPEX (R)", 0, 10_000_000, 1_000_000, step=10000)
opex = st.sidebar.number_input("Annual OPEX (R)", 0, 2_000_000, 200_000, step=10000)
revenue = st.sidebar.number_input("Initial Annual Revenue (R)", 0, 5_000_000, 500_000, step=10000)
growth = st.sidebar.slider("Annual Revenue Growth Rate (%)", 0.0, 0.5, 0.10)
discount = st.sidebar.slider("Discount Rate (%)", 0.0, 0.25, 0.10)

st.sidebar.markdown("---")
n_sims = st.sidebar.slider("Monte Carlo Simulations", 100, 5000, 1000, step=100)
run_sim = st.sidebar.button("Run Monte Carlo Simulation")

# --- Helper Functions ---
def npv(rate, cashflows):
    return np.sum([cf / (1 + rate)**t for t, cf in enumerate(cashflows, start=1)])

def irr(cashflows):
    try:
        return np.irr(cashflows)
    except Exception:
        return np.nan

def payback_period(cashflows):
    cumulative = np.cumsum(cashflows)
    for i, val in enumerate(cumulative):
        if val >= 0:
            prev = cumulative[i-1] if i > 0 else 0
            return i + abs(prev) / cashflows[i]
    return np.nan

# --- Default 10-year Projection Table ---
df = pd.DataFrame({
    "Year": range(1, years + 1),
    "CAPEX (R)": [capex if i == 1 else 0 for i in range(1, years + 1)],
    "OPEX (R)": [opex] * years,
    "Revenue (R)": [revenue * (1 + growth)**(i - 1) for i in range(1, years + 1)],
})
df["Net Cashflow (R)"] = df["Revenue (R)"] - df["OPEX (R)"] - df["CAPEX (R)"]

st.subheader("📅 Editable 10-Year Financial Projection")
st.markdown("You can adjust any value directly in the table below to test new scenarios.")
edited_df = st.data_editor(df, num_rows="fixed", use_container_width=True)

# --- Calculations from edited data ---
cashflows = edited_df["Net Cashflow (R)"].tolist()
base_npv = npv(discount, cashflows)
base_irr = irr(cashflows)
base_payback = payback_period(cashflows)

# --- Display Key Metrics ---
st.subheader("📊 Key Financial Metrics (Auto-updated)")
col1, col2, col3 = st.columns(3)
col1.metric("NPV (R)", f"{base_npv:,.0f}")
col2.metric("IRR (%)", f"{(base_irr*100 if base_irr else 0):.1f}")
col3.metric("Payback Period (years)", f"{base_payback:.1f}")

# --- Smaller Chart (Half-width) ---
col_chart, _ = st.columns([1.2, 1])
with col_chart:
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(edited_df["Year"], np.cumsum(edited_df["Net Cashflow (R)"]), marker="o", color="teal")
    ax.axhline(0, color="red", linestyle="--")
    ax.set_xlabel("Year")
    ax.set_ylabel("Cumulative Cashflow (R)")
    ax.set_title("Cumulative Cashflow Projection")
    ax.grid(True, linestyle="--", alpha=0.6)
    st.pyplot(fig)

# --- Monte Carlo Simulation ---
if run_sim:
    npvs = []
    for _ in range(n_sims):
        rev_mult = np.random.uniform(0.8, 1.2)
        cost_mult = np.random.uniform(0.8, 1.2)
        growth_mult = np.random.uniform(0.8, 1.2)
        rate_mult = np.random.uniform(0.9, 1.1)

        sim_df = edited_df.copy()
        sim_df["Revenue (R)"] = sim_df["Revenue (R)"] * rev_mult * (1 + growth_mult * (sim_df["Year"] - 1))
        sim_df["OPEX (R)"] = sim_df["OPEX (R)"] * cost_mult
        sim_df["Net Cashflow (R)"] = sim_df["Revenue (R)"] - sim_df["OPEX (R)"] - sim_df["CAPEX (R)"]

        npvs.append(npv(discount * rate_mult, sim_df["Net Cashflow (R)"].tolist()))

    npvs = np.array(npvs)
    success_prob = np.mean(npvs > 0) * 100

    st.subheader("🎲 Monte Carlo Simulation Results")
    st.write(f"**{success_prob:.1f}%** of simulations resulted in a positive NPV.")
    st.write(f"Mean NPV: R{np.mean(npvs):,.0f} ± R{np.std(npvs):,.0f}")

    fig2, ax2 = plt.subplots(figsize=(6, 3))
    ax2.hist(npvs, bins=40, color="skyblue", edgecolor="black")
    ax2.axvline(np.mean(npvs), color="green", linestyle="--", label="Mean NPV")
    ax2.axvline(0, color="red", linestyle="--", label="Break-even")
    ax2.set_xlabel("NPV (R)")
    ax2.set_ylabel("Frequency")
    ax2.legend()
    st.pyplot(fig2)

# --- Learn Section ---
with st.expander("📘 Learn about Financial Metrics"):
    st.markdown(
        """
        **NPV (Net Present Value)** — The sum of discounted future cash flows; positive NPV means the project adds value.  
        **IRR (Internal Rate of Return)** — The discount rate where NPV = 0; higher IRR indicates better return potential.  
        **Payback Period** — How long it takes for cumulative cashflows to become positive.  
        **Monte Carlo Simulation** — A risk analysis technique that runs thousands of random variations to show probability of success.
        """
    )
