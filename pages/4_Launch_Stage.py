import numpy as np
import streamlit as st

st.subheader("📊 Financial Metrics Demo Calculators")
st.markdown("""
Understand key investment metrics used by funders, investors, and decision-makers.  
Use the simple tools below to test how each metric responds to changes in your inputs.
""")

# ----------------
# ROI
# ----------------
with st.expander("💰 ROI (Return on Investment)"):
    gain = st.number_input("Total Revenue (R)", value=200000, key="roi_gain")
    cost = st.number_input("Total Cost (R)", value=100000, key="roi_cost")
    if cost > 0:
        roi = (gain - cost) / cost * 100
        st.success(f"**ROI = {roi:.2f}%**\n\nROI shows how much profit you earn for every R1 invested.")

# ----------------
# IRR
# ----------------
with st.expander("📈 IRR (Internal Rate of Return)"):
    st.write("Enter cashflows including the initial investment as a negative number.")
    flows = st.text_input("Cashflows (comma-separated)", "-100000, 20000, 30000, 50000, 70000", key="irr_flows")
    try:
        cashflows = [float(x.strip()) for x in flows.split(",")]
        irr = np.irr(cashflows)
        if irr is not None:
            st.success(f"**IRR ≈ {irr*100:.2f}%**\n\nIRR shows the average annual growth rate of your investment.")
    except:
        st.error("Enter valid numbers")

# ----------------
# NPV
# ----------------
with st.expander("💸 NPV (Net Present Value)"):
    st.write("Enter future cashflows and a discount rate (cost of capital).")
    cash = st.text_input("Cashflows (comma-separated)", "-100000, 20000, 30000, 50000, 70000", key="npv_flows")
    discount = st.number_input("Discount Rate (%)", value=10.0, key="npv_rate") / 100
    try:
        flows = [float(x.strip()) for x in cash.split(",")]
        years = np.arange(len(flows))
        npv = np.sum([cf / (1+discount)**t for cf, t in zip(flows, years)])
        st.success(f"**NPV = R{npv:,.2f}**\n\nNPV shows the value of all future profits in today’s money.")
    except:
        st.error("Enter valid numbers")

# ----------------
# LCOE
# ----------------
with st.expander("⚡ LCOE (Levelised Cost of Energy)"):
    st.write("For energy projects: average cost per kWh over the system's lifetime.")
    total_costs = st.number_input("Total Lifetime Costs (R)", value=500000, key="lcoe_cost")
    energy_output = st.number_input("Lifetime Energy Output (kWh)", value=100000, key="lcoe_output")
    if energy_output > 0:
        lcoe = total_costs / energy_output
        st.success(f"**LCOE = R{lcoe:.2f} per kWh**\n\nLCOE lets you compare the cost of different energy systems fairly.")
