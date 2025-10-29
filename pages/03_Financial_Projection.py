import streamlit as st
import numpy as np
import pandas as pd
import io
import json

st.set_page_config(page_title="Financial Projection Sandbox", layout="wide")
st.title("💰 Financial Projection Sandbox (Phase 1.8)")

# ----------------------------
# Sidebar Inputs (baseline)
# ----------------------------
st.sidebar.header("Input Parameters")
years = st.sidebar.slider("Projection Period (years)", 1, 15, 10)
capex = st.sidebar.number_input("Initial CAPEX (R)", 0, 50_000_000, 1_000_000, step=50_000)
opex = st.sidebar.number_input("Annual OPEX (R)", 0, 10_000_000, 200_000, step=10_000)
revenue = st.sidebar.number_input("Initial Annual Revenue (R)", 0, 20_000_000, 500_000, step=10_000)
growth = st.sidebar.slider("Annual Revenue Growth Rate (%)", 0.0, 0.8, 0.10, step=0.01)
discount = st.sidebar.slider("Discount Rate (%)", 0.0, 0.30, 0.10, step=0.005)

st.sidebar.markdown("---")
n_sims = st.sidebar.slider("Monte Carlo Simulations", 100, 10000, 2000, step=100)
run_sim = st.sidebar.button("Run Monte Carlo Simulation")

# ----------------------------
# Helper functions
# ----------------------------
def npv(rate: float, cashflows: list[float]) -> float:
    # cashflows are assumed at the end of each year (t = 1..N)
    return float(np.sum([cf / (1.0 + rate)**t for t, cf in enumerate(cashflows, start=1)]))

def irr_bisection(cashflows: list[float], lo: float = -0.99, hi: float = 5.0, tol: float = 1e-6, max_iter: int = 200):
    """
    Robust IRR via bisection on NPV(r).
    cashflows: include Year 0 flow at index 0 (usually negative CAPEX), then years 1..N.
    Returns annualized rate or np.nan if not solvable.
    """
    def npv0(r):
        return sum(cf / ((1 + r) ** t) for t, cf in enumerate(cashflows, start=0))
    f_lo, f_hi = npv0(lo), npv0(hi)
    if np.isnan(f_lo) or np.isnan(f_hi) or f_lo * f_hi > 0:
        return np.nan
    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        f_mid = npv0(mid)
        if abs(f_mid) < tol:
            return mid
        if f_lo * f_mid < 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return np.nan

def payback_period(cashflows: list[float]):
    """
    cashflows include Year 0 at index 0 (likely negative), then years 1..N.
    Returns fractional year where cumulative turns non-negative, else None.
    """
    cumulative = np.cumsum(cashflows)
    for i in range(1, len(cashflows)):
        if cumulative[i] >= 0:
            prev = cumulative[i-1]
            delta = cashflows[i]
            if delta == 0:
                return float(i)
            frac = 1.0 - (prev / delta)  # linear interpolation within the year
            return float(i - 1 + frac)
    return None

def make_autofill_df(years, capex, opex, revenue, growth):
    df = pd.DataFrame({
        "Year": range(1, years + 1),
        "CAPEX (R)": [capex] + [0]*(years - 1),
        "OPEX (R)": [opex]*years,
        "Revenue (R)": [revenue * (1 + growth)**(i - 1) for i in range(1, years + 1)],
    })
    df["Net Cashflow (R)"] = df["Revenue (R)"] - df["OPEX (R)"] - df["CAPEX (R)"]
    return df

def to_excel_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Projection")
    return buf.getvalue()

def solve_revenue_for_npv0(df: pd.DataFrame, discount: float, lo=0.1, hi=5.0, tol=1e-6, max_iter=80):
    """
    Returns a factor 'k' to multiply all Revenue rows so that NPV ≈ 0.
    If not solvable, returns None.
    """
    base_rev = df["Revenue (R)"].to_numpy()
    fixed = (df["Revenue (R)"]*0 - df["OPEX (R)"] - df["CAPEX (R)"]).to_numpy()  # -OPEX - CAPEX
    # Year 0 flow (index 0) equals negative CAPEX in year 1 row moved to time 0? We currently keep CAPEX in year 1.
    # We'll keep current structure (flows at years 1..N), consistent with npv() use.

    def f(k):
        flows = (k * base_rev + fixed).tolist()
        return npv(discount, flows)

    f_lo, f_hi = f(lo), f(hi)
    if np.isnan(f_lo) or np.isnan(f_hi) or f_lo * f_hi > 0:
        return None
    for _ in range(max_iter):
        mid = 0.5*(lo + hi)
        f_mid = f(mid)
        if abs(f_mid) < tol:
            return mid
        if f_lo * f_mid < 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return None

# ----------------------------
# Editable 10-year table
# ----------------------------
st.subheader("📅 Editable 10-Year Financial Projection")

if "fp_df" not in st.session_state:
    st.session_state.fp_df = make_autofill_df(years, capex, opex, revenue, growth)

# Controls above table
c1, c2, c3 = st.columns([1,1,2])
with c1:
    if st.button("🔄 Auto-fill from inputs"):
        st.session_state.fp_df = make_autofill_df(years, capex, opex, revenue, growth)
with c2:
    if st.button("♻️ Reset (zeros except Year 1 CAPEX)"):
        df = pd.DataFrame({
            "Year": range(1, years + 1),
            "CAPEX (R)": [capex] + [0]*(years - 1),
            "OPEX (R)": [0]*years,
            "Revenue (R)": [0]*years
        })
        df["Net Cashflow (R)"] = df["Revenue (R)"] - df["OPEX (R)"] - df["CAPEX (R)"]
        st.session_state.fp_df = df

# If years changed since stored, resize
if len(st.session_state.fp_df) != years:
    st.session_state.fp_df = make_autofill_df(years, capex, opex, revenue, growth)

# Show guidance tooltips for columns
with st.expander("ℹ️ Column guide (tap to expand)"):
    st.markdown(
        "- **CAPEX (R)**: Once-off capital per year (often only Year 1).\n"
        "- **OPEX (R)**: Recurring operating costs (staff, maintenance, energy, etc.).\n"
        "- **Revenue (R)**: Sales/fees in that year.\n"
        "- **Net Cashflow (R)**: Auto = Revenue − OPEX − CAPEX (editable if needed)."
    )

# Data editor
edited_df = st.data_editor(
    st.session_state.fp_df,
    num_rows="fixed",
    use_container_width=True,
    hide_index=True
)

# Recompute Net Cashflow if user altered the three components (keep user edits if they directly changed Net Cashflow)
auto_recompute = st.toggle("Auto-recompute Net Cashflow from Revenue/OPEX/CAPEX", value=True, help="If on, Net Cashflow is always recalculated as Revenue − OPEX − CAPEX.")
if auto_recompute:
    edited_df["Net Cashflow (R)"] = edited_df["Revenue (R)"] - edited_df["OPEX (R)"] - edited_df["CAPEX (R)"]

# Persist
st.session_state.fp_df = edited_df.copy()

# ----------------------------
# Metrics from current table
# ----------------------------
flows = edited_df["Net Cashflow (R)"].tolist()
# For IRR & Payback, include a Year 0 flow of 0 (since your CAPEX is in Year 1 row). Many practitioners put CAPEX in Year 0.
# If you prefer CAPEX at t=0, move it there; for now, keep consistent with NPV usage (flows at t=1..N).
irr_val = irr_bisection([0.0] + flows)
npv_val = npv(discount, flows)
payback = payback_period([0.0] + flows)

st.subheader("📊 Key Financial Metrics (Auto-updated)")
m1, m2, m3, m4 = st.columns(4)
m1.metric("NPV (R)", f"{npv_val:,.0f}")
m2.metric("IRR (%)", f"{(irr_val*100 if not np.isnan(irr_val) else 0):.1f}")
m3.metric("Payback (yrs)", f"{payback:.1f}" if payback is not None else "—")
m4.metric("Profitability Index", f"{(npv_val / max(1.0, edited_df['CAPEX (R)'].sum())):,.2f}")

# Quick helper: required revenue multiplier for NPV ~ 0
k = solve_revenue_for_npv0(edited_df, discount)
if k is not None:
    st.info(f"📈 To achieve NPV ≈ 0 at a {discount*100:.1f}% discount rate, your revenues would need to be about **×{k:.2f}** current values (uniformly across years).")
else:
    st.info("📈 Could not find a stable revenue multiplier for NPV ≈ 0 (try adjusting assumptions).")

# ----------------------------
# Mentor guidance (thresholds)
# ----------------------------
with st.expander("🧠 Mentor Tips & Guidance"):
    tips = []
    # IRR guidance
    if np.isnan(irr_val) or irr_val < 0.08:
        tips.append("⚠️ **Low IRR (< 8%)** — may struggle to attract investors. Improve revenue or reduce OPEX/CAPEX.")
    elif irr_val < 0.15:
        tips.append("ℹ️ **Moderate IRR (8–15%)** — borderline for commercial funds; grants/blended finance may help.")
    else:
        tips.append("🚀 **Strong IRR (> 15%)** — attractive for many investors.")

    # Payback
    if payback is None:
        tips.append("⚠️ **No payback in horizon** — consider longer period or better unit economics.")
    elif payback > 10:
        tips.append("⏳ **Long payback (>10 years)** — high risk; try phasing CAPEX or improving early margins.")
    elif payback > 5:
        tips.append("🕐 **Payback (5–10 years)** — acceptable in infrastructure; consider performance contracts.")
    else:
        tips.append("✅ **Fast payback (<5 years)** — investor-friendly profile.")

    # Cost structure
    rev_sum = float(edited_df["Revenue (R)"].sum())
    opex_sum = float(edited_df["OPEX (R)"].sum())
    if rev_sum > 0:
        opex_share = opex_sum / rev_sum
        if opex_share > 0.8:
            tips.append("📉 **OPEX > 80% of revenue** — tighten costs or improve pricing.")
        elif opex_share > 0.6:
            tips.append("🟠 **OPEX ~60–80% of revenue** — okay but watch margins.")
        else:
            tips.append("🟢 **Healthy cost structure** — OPEX < 60% of revenue.")

    for t in tips:
        st.markdown("- " + t)

# ----------------------------
# Compact Charts
# ----------------------------
st.subheader("📈 Visuals")
c1, c2 = st.columns(2)

with c1:
    st.caption("Cumulative Cashflow")
    cum = np.cumsum(flows)
    chart_df = pd.DataFrame({"Year": edited_df["Year"], "Cumulative Cashflow (R)": cum})
    st.line_chart(chart_df, x="Year", y="Cumulative Cashflow (R)", use_container_width=True)

with c2:
    st.caption("Revenue vs OPEX")
    rev_opex_df = pd.DataFrame({
        "Year": edited_df["Year"],
        "Revenue (R)": edited_df["Revenue (R)"],
        "OPEX (R)": edited_df["OPEX (R)"]
    })
    st.line_chart(rev_opex_df.set_index("Year"), use_container_width=True)

# ----------------------------
# Monte Carlo (no external plotting libs)
# ----------------------------
if run_sim:
    npvs = []
    # define randomness ranges (edit as needed)
    for _ in range(n_sims):
        # independent random multipliers
        rev_mult = np.random.uniform(0.85, 1.20)
        opex_mult = np.random.uniform(0.85, 1.20)
        # mild trend on growth by year (optional): 1 + 0.02*(year-1) etc. We keep simple.
        rate_mult = np.random.uniform(0.90, 1.10)

        sim = edited_df.copy()
        sim["Revenue (R)"] = sim["Revenue (R)"] * rev_mult
        sim["OPEX (R)"] = sim["OPEX (R)"] * opex_mult
        sim["Net Cashflow (R)"] = sim["Revenue (R)"] - sim["OPEX (R)"] - sim["CAPEX (R)"]

        npvs.append(npv(discount * rate_mult, sim["Net Cashflow (R)"].tolist()))

    npvs = np.array(npvs, dtype=float)
    success_prob = float(np.mean(npvs > 0) * 100.0)
    mean_npv = float(np.mean(npvs))
    p25, p50, p75 = np.percentile(npvs, [25, 50, 75])

    st.subheader("🎲 Monte Carlo Results")
    st.write(
        f"**{success_prob:.1f}%** of simulations resulted in a **positive NPV**.  \n"
        f"Mean NPV: **R{mean_npv:,.0f}**, Median: **R{p50:,.0f}**  \n"
        f"Most likely range (IQR): **R{p25:,.0f} – R{p75:,.0f}**"
    )

    # Histogram without matplotlib: use numpy histogram + bar_chart
    hist_counts, bin_edges = np.histogram(npvs, bins=40)
    midpoints = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    hist_df = pd.DataFrame({"NPV bin mid": midpoints, "Count": hist_counts})
    st.bar_chart(hist_df.set_index("NPV bin mid"), use_container_width=True)

# ----------------------------
# Save / Load / Export
# ----------------------------
st.subheader("📤 Save, Load, Export")

colA, colB, colC = st.columns(3)
with colA:
    # Save scenario JSON (inputs + table)
    scenario = {
        "years": years, "capex": capex, "opex": opex, "revenue": revenue,
        "growth": growth, "discount": discount,
        "table": edited_df.to_dict(orient="list")
    }
    st.download_button(
        "💾 Save Scenario (JSON)",
        data=json.dumps(scenario, indent=2),
        file_name="financial_scenario.json",
        mime="application/json",
        use_container_width=True
    )

with colB:
    # Load scenario JSON
    up = st.file_uploader("Load Scenario (JSON)", type=["json"])
    if up is not None:
        try:
            sc = json.loads(up.read().decode("utf-8"))
            # Rebuild dataframe
            t = sc.get("table", {})
            if t:
                st.session_state.fp_df = pd.DataFrame(t)
                st.success("Scenario loaded.")
            # Note: not auto-overwriting sidebar inputs to avoid jarring UI changes
        except Exception as e:
            st.error(f"Failed to load scenario: {e}")

with colC:
    # Download Excel
    xls = to_excel_bytes(edited_df)
    st.download_button(
        "⬇️ Download Projection (Excel)",
        data=xls,
        file_name="projection_10y.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

# ----------------------------
# Learn block
# ----------------------------
with st.expander("📘 Learn: What these metrics mean"):
    st.markdown(
        """
**NPV (Net Present Value)** — Value created after discounting future cash flows.  
**IRR (Internal Rate of Return)** — The discount rate where NPV = 0 (annualized).  
**Payback Period** — How long until cumulative cashflows turn positive.  
**Profitability Index** — Efficiency of CAPEX use (NPV ÷ CAPEX).  
**Monte Carlo** — Repeats the model with random variations to estimate risk.
"""
    )

