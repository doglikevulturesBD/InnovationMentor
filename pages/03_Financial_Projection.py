import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Financial Projection Sandbox", layout="wide")

st.title("💰 Financial Projection Sandbox (Phase 1)")

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

# --- Base Case Calculation ---
base_revenues = [revenue * (1 + growth)**t for t in range(years)]
base_costs = [opex for _ in range(years)]
cashflows = [r - c for r, c in zip(base_revenues, base_costs)]
cashflows[0] -= capex

base_npv = npv(discount, cashflows)
base_irr = irr([-capex] + cashflows)
base_payback = payback_period([-capex] + cashflows)

# --- Display Key Metrics ---
st.subheader("📊 Base Case Results")
col1, col2, col3 = st.columns(3)
col1.metric("NPV (R)", f"{base_npv:,.0f}")
col2.metric("IRR (%)", f"{(base_irr*100 if base_irr else 0):.1f}")
col3.metric("Payback Period (years)", f"{base_payback:.1f}")

# --- Chart ---
fig, ax = plt.subplots()
ax.plot(range(1, years+1), np.cumsum(cashflows), label="Cumulative Cashflow")
ax.axhline(0, color='red', linestyle='--')
ax.set_xlabel("Year")
ax.set_ylabel("Cumulative Cashflow (R)")
ax.legend()
st.pyplot(fig)

# --- Monte Carlo Simulation ---
if run_sim:
    npvs = []
    for _ in range(n_sims):
        rev_mult = np.random.uniform(0.8, 1.2)
        cost_mult = np.random.uniform(0.8, 1.2)
        growth_mult = np.random.uniform(0.8, 1.2)
        rate_mult = np.random.uniform(0.9, 1.1)

        sim_revenue = revenue * rev_mult
        sim_opex = opex * cost_mult
        sim_growth = growth * growth_mult
        sim_discount = discount * rate_mult

        sim_revenues = [sim_revenue * (1 + sim_growth)**t for t in range(years)]
        sim_costs = [sim_opex for _ in range(years)]
        sim_cashflows = [r - c for r, c in zip(sim_revenues, sim_costs)]
        sim_cashflows[0] -= capex

        npvs.append(npv(sim_discount, sim_cashflows))

    npvs = np.array(npvs)
    success_prob = np.mean(npvs > 0) * 100

    st.subheader("🎲 Monte Carlo Results")
    st.write(f"**{success_prob:.1f}%** of simulations resulted in a positive NPV.")
    st.write(f"Mean NPV: R{np.mean(npvs):,.0f} ± R{np.std(npvs):,.0f}")

    fig2, ax2 = plt.subplots()
    ax2.hist(npvs, bins=40, color='skyblue', edgecolor='black')
    ax2.axvline(np.mean(npvs), color='green', linestyle='--', label='Mean NPV')
    ax2.axvline(0, color='red', linestyle='--', label='Break-even')
    ax2.set_xlabel("NPV (R)")
    ax2.set_ylabel("Frequency")
    ax2.legend()
    st.pyplot(fig2)

# --- Learn Section ---
with st.expander("📘 Learn about Financial Metrics"):
    st.markdown("""
    **NPV (Net Present Value)** — The sum of discounted future cash flows; positive NPV means the project adds value.

    **IRR (Internal Rate of Return)** — The discount rate where NPV = 0; higher IRR indicates better return potential.

    **Payback Period** — How long it takes for cumulative cashflows to become positive.

    **Monte Carlo Simulation** — A risk analysis technique that runs thousands of random variations to show probability of success.
    """)
