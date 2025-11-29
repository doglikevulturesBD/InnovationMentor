import streamlit as st
import numpy as np
import pandas as pd
import io
from datetime import datetime
import streamlit as st

# -------- Header --------
st.title("Financial Projections")



# ------------------------
# Sidebar Inputs
# ------------------------
st.sidebar.header("Global Assumptions")
years = st.sidebar.slider("Projection Years", 5, 15, 10)
discount = st.sidebar.slider("Discount Rate (%)", 0.0, 0.3, 0.1, step=0.005)

st.sidebar.markdown("---")
st.sidebar.caption("Unit Economics (Baseline)")
units_y1 = st.sidebar.number_input("Units sold (Year 1)", 0, 10_000_000, 1000, step=50)
price = st.sidebar.number_input("Price per unit (R)", 0, 10_000_000, 5000, step=50)
cogs = st.sidebar.number_input("COGS per unit (R)", 0, 10_000_000, 3000, step=50)
opex_fixed = st.sidebar.number_input("Fixed OPEX per year (R)", 0, 20_000_000, 200_000, step=10_000)
capex_y1 = st.sidebar.number_input("CAPEX (Year 1) (R)", 0, 100_000_000, 1_000_000, step=50_000)
growth = st.sidebar.slider("Units Growth per year (%)", 0.0, 1.0, 0.10, step=0.01)

st.sidebar.markdown("---")
st.sidebar.caption("Scenario Sensitivity")
rev_up = st.sidebar.slider("Optimistic: Revenue +%", 0.0, 0.5, 0.20, step=0.01)
cost_down = st.sidebar.slider("Optimistic: Costs -%", 0.0, 0.5, 0.10, step=0.01)
rev_down = st.sidebar.slider("Pessimistic: Revenue -%", 0.0, 0.5, 0.20, step=0.01)
cost_up = st.sidebar.slider("Pessimistic: Costs +%", 0.0, 0.5, 0.10, step=0.01)

st.sidebar.markdown("---")
n_sims = st.sidebar.slider("Monte Carlo Samples per scenario", 100, 5000, 1000, step=100)

# ------------------------
# Helper functions
# ------------------------
def make_units(y1, growth, years):
    return np.array([int(round(y1 * (1 + growth)**i)) for i in range(years)])

def build_df(units, price, cogs, opex, capex_y1):
    years = len(units)
    capex = np.zeros(years)
    capex[0] = capex_y1
    revenue = units * price
    cogs_total = units * cogs
    net = revenue - cogs_total - opex - capex
    return pd.DataFrame({
        "Year": np.arange(1, years + 1),
        "Units": units,
        "Price (R/u)": price,
        "COGS (R/u)": cogs,
        "Revenue (R)": revenue,
        "COGS (R)": cogs_total,
        "OPEX (R)": opex,
        "CAPEX (R)": capex,
        "Net Cashflow (R)": net
    })

def recompute(df):
    df = df.copy()
    df["Revenue (R)"] = df["Units"] * df["Price (R/u)"]
    df["COGS (R)"] = df["Units"] * df["COGS (R/u)"]
    df["Net Cashflow (R)"] = df["Revenue (R)"] - df["COGS (R)"] - df["OPEX (R)"] - df["CAPEX (R)"]
    return df

def npv(rate, flows):
    return np.sum([cf / (1 + rate)**t for t, cf in enumerate(flows, start=1)])

def irr(flows):
    lo, hi = -0.99, 5.0
    for _ in range(200):
        mid = (lo + hi) / 2
        npv_mid = sum(cf / (1 + mid)**t for t, cf in enumerate(flows, start=0))
        npv_lo = sum(cf / (1 + lo)**t for t, cf in enumerate(flows, start=0))
        if npv_mid == 0 or abs(npv_mid) < 1e-6:
            return mid
        if npv_lo * npv_mid < 0:
            hi = mid
        else:
            lo = mid
    return 0.0

def payback(flows):
    cum = np.cumsum(flows)
    for i in range(1, len(flows)):
        if cum[i] >= 0:
            prev = cum[i-1]
            delta = flows[i]
            return i - 1 + (abs(prev) / delta)
    return None

def success_prob(df, discount, n):
    base_flows = df["Net Cashflow (R)"].to_numpy()
    rev = df["Revenue (R)"].to_numpy()
    cost = (df["COGS (R)"] + df["OPEX (R)"] + df["CAPEX (R)"]).to_numpy()
    rng = np.random.default_rng()
    success = 0
    for _ in range(n):
        rev_mult = rng.uniform(0.8, 1.2)
        cost_mult = rng.uniform(0.85, 1.15)
        rate_mult = rng.uniform(0.9, 1.1)
        sim_flows = (rev * rev_mult - cost * cost_mult)
        if npv(discount * rate_mult, sim_flows) > 0:
            success += 1
    return success / n * 100

def metrics(df, discount):
    flows = df["Net Cashflow (R)"].tolist()
    # Move CAPEX of Year 1 to time 0
    irr_val = irr([-float(df["CAPEX (R)"].iloc[0])] + flows[1:])
    return {
        "NPV": npv(discount, flows),
        "IRR": irr_val,
        "Payback": payback([-float(df["CAPEX (R)"].iloc[0])] + flows[1:]),
        "PI": npv(discount, flows) / max(1, df["CAPEX (R)"].sum())
    }

def scenario(df, mode):
    df = df.copy()
    if mode == "optimistic":
        df["Price (R/u)"] *= (1 + rev_up)
        df["COGS (R/u)"] *= (1 - cost_down)
    elif mode == "pessimistic":
        df["Price (R/u)"] *= (1 - rev_down)
        df["COGS (R/u)"] *= (1 + cost_up)
    return recompute(df)

# ------------------------
# Default dataframes
# ------------------------
units = make_units(units_y1, growth, years)
baseline_default = build_df(units, price, cogs, opex_fixed, capex_y1)
optimistic_default = scenario(baseline_default, "optimistic")
pessimistic_default = scenario(baseline_default, "pessimistic")

# Ensure state
for key, df_default in [
    ("df_base", baseline_default),
    ("df_opt", optimistic_default),
    ("df_pes", pessimistic_default)
]:
    if key not in st.session_state or len(st.session_state[key]) != years:
        st.session_state[key] = df_default.copy()

tabs = st.tabs(["Baseline", "Optimistic", "Pessimistic", "Summary"])

# ------------------------
# Scenario tab component
# ------------------------
def scenario_tab(label, key, default_df):
    st.markdown(f"### {label} Scenario")
    c1, c2 = st.columns([1,1])
    with c1:
        if st.button("🔄 Refill from assumptions", key=f"refill_{key}"):
            st.session_state[key] = default_df.copy()
    with c2:
        if st.button("♻️ Reset table", key=f"reset_{key}"):
            df = default_df.copy()
            df["Units"] = 0
            df["Price (R/u)"] = 0
            df["COGS (R/u)"] = 0
            df["OPEX (R)"] = 0
            df["Revenue (R)"] = 0
            df["COGS (R)"] = 0
            df["Net Cashflow (R)"] = 0
            df["CAPEX (R)"].iloc[0] = capex_y1
            st.session_state[key] = df

    st.caption("Edit Units, Price, COGS, OPEX, and CAPEX only. Net Cashflow is calculated automatically.")

    df = st.session_state[key]
    editable_cols = [c for c in df.columns if c != "Net Cashflow (R)"]
    edited = st.data_editor(
        df,
        use_container_width=True,
        num_rows="fixed",
        hide_index=True,
        disabled=["Net Cashflow (R)"]
    )

    edited = recompute(edited)
    st.session_state[key] = edited.copy()

    mets = metrics(edited, discount)
    prob = success_prob(edited, discount, n_sims)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("NPV (R)", f"{mets['NPV']:,.0f}")
    c2.metric("IRR (%)", f"{mets['IRR']*100:.1f}")
    c3.metric("Payback (yrs)", f"{mets['Payback']:.1f}" if mets['Payback'] else "—")
    c4.metric("PI", f"{mets['PI']:.2f}")
    c5.metric("Success Prob. (%)", f"{prob:.1f}")

    with st.expander("Mentor Tips"):
        tips = []
        if mets["IRR"] < 0.08:
            tips.append("IRR below 8% — tough sell to investors.")
        elif mets["IRR"] < 0.15:
            tips.append("IRR 8–15% — fair; suitable for grants/blended funds.")
        else:
            tips.append("IRR above 15% — attractive investment profile.")
        if mets["Payback"] and mets["Payback"] > 10:
            tips.append("Payback >10 years — consider phasing CAPEX.")
        elif mets["Payback"] and mets["Payback"] > 5:
            tips.append("Payback 5–10 years — typical for infra projects.")
        else:
            tips.append("Payback <5 years — highly investable.")
        tips.append(f"Success Probability {prob:.0f}% (based on {n_sims} simulations).")
        for t in tips:
            st.markdown("- " + t)

    return edited, mets, prob

with tabs[0]:
    df_base, mets_base, prob_base = scenario_tab("Baseline", "df_base", baseline_default)
with tabs[1]:
    df_opt, mets_opt, prob_opt = scenario_tab("Optimistic", "df_opt", optimistic_default)
with tabs[2]:
    df_pes, mets_pes, prob_pes = scenario_tab("Pessimistic", "df_pes", pessimistic_default)

# ------------------------
# Summary
# ------------------------
with tabs[3]:
    st.subheader("📊 Scenario Summary")
    summary = pd.DataFrame([
        ["Baseline", mets_base["NPV"], mets_base["IRR"]*100, mets_base["Payback"], mets_base["PI"], prob_base],
        ["Optimistic", mets_opt["NPV"], mets_opt["IRR"]*100, mets_opt["Payback"], mets_opt["PI"], prob_opt],
        ["Pessimistic", mets_pes["NPV"], mets_pes["IRR"]*100, mets_pes["Payback"], mets_pes["PI"], prob_pes]
    ], columns=["Scenario", "NPV (R)", "IRR (%)", "Payback (yrs)", "PI", "Success Prob. (%)"])
    st.dataframe(summary.style.format({
        "NPV (R)": "{:,.0f}",
        "IRR (%)": "{:.1f}",
        "Payback (yrs)": "{:.1f}",
        "PI": "{:.2f}",
        "Success Prob. (%)": "{:.1f}"
    }), hide_index=True, use_container_width=True)

    # --- PDF export ---
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import cm

    def make_pdf():
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        width, height = A4
        t = c.beginText(2*cm, height - 2*cm)
        t.setFont("Helvetica", 10)
        t.textLine(f"Financial Projection Summary — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        t.textLine("")
        for row in summary.itertuples(index=False):
            t.textLine(f"{row[0]}: NPV R{row[1]:,.0f} | IRR {row[2]:.1f}% | Payback {row[3]:.1f} yrs | PI {row[4]:.2f} | Success {row[5]:.1f}%")
        c.drawText(t)
        c.showPage()
        c.save()
        pdf = buf.getvalue()
        buf.close()
        return pdf

    st.download_button("⬇️ Download PDF Summary", make_pdf(),
                       file_name="financial_projection_summary.pdf",
                       mime="application/pdf",
                       use_container_width=True)
