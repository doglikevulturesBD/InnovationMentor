import streamlit as st
import numpy as np
import pandas as pd
import io
import json
from datetime import datetime

st.set_page_config(page_title="Financial Projection (Scenarios)", layout="wide")
st.title("💰 Financial Projection — Baseline / Optimistic / Pessimistic (v2.0)")

# =============================
# Sidebar: Global Assumptions
# =============================
st.sidebar.header("Global Assumptions")

years = st.sidebar.slider("Projection Years", 5, 15, 10)
discount = st.sidebar.slider("Discount Rate (%)", 0.00, 0.30, 0.10, step=0.005)

st.sidebar.markdown("---")
st.sidebar.caption("Unit Economics (Baseline)")
units_y1 = st.sidebar.number_input("Units sold (Year 1)", 0, 10_000_000, 1_000, step=50)
price = st.sidebar.number_input("Price per unit (R)", 0, 10_000_000, 5_000, step=50)
cogs = st.sidebar.number_input("COGS per unit (R)", 0, 10_000_000, 3_000, step=50)
opex_fixed = st.sidebar.number_input("Fixed OPEX per year (R)", 0, 20_000_000, 200_000, step=10_000)
capex_y1 = st.sidebar.number_input("CAPEX (Year 1) (R)", 0, 100_000_000, 1_000_000, step=50_000)
annual_units_growth = st.sidebar.slider("Units Growth per year (%)", 0.0, 1.0, 0.10, step=0.01)

st.sidebar.markdown("---")
st.sidebar.caption("Scenario Sensitivity (applied before random variation)")
rev_up = st.sidebar.slider("Optimistic: Revenue +%", 0.0, 0.5, 0.20, step=0.01)
cost_down = st.sidebar.slider("Optimistic: Costs -%", 0.0, 0.5, 0.10, step=0.01)
rev_down = st.sidebar.slider("Pessimistic: Revenue -%", 0.0, 0.5, 0.20, step=0.01)
cost_up = st.sidebar.slider("Pessimistic: Costs +%", 0.0, 0.5, 0.10, step=0.01)

st.sidebar.markdown("---")
st.sidebar.caption("Success Probability (Monte Carlo)")
n_sims = st.sidebar.slider("Simulations per scenario", 100, 5000, 1000, step=100)

# =============================
# Helpers
# =============================
def make_units_vector(y1_units: int, growth: float, years: int) -> np.ndarray:
    return np.array([int(round(y1_units * (1.0 + growth)**(i))) for i in range(years)])

def build_df_from_units(units_vec: np.ndarray,
                        price: float,
                        cogs: float,
                        opex_fixed: float,
                        capex_y1: float) -> pd.DataFrame:
    years = len(units_vec)
    revenue = units_vec * price
    cogs_cost = units_vec * cogs
    capex = np.zeros(years, dtype=float)
    capex[0] = capex_y1
    opex = np.full(years, float(opex_fixed))
    net = revenue - cogs_cost - opex - capex
    df = pd.DataFrame({
        "Year": np.arange(1, years + 1),
        "Units": units_vec,
        "Price (R/u)": np.full(years, price, dtype=float),
        "COGS (R/u)": np.full(years, cogs, dtype=float),
        "Revenue (R)": revenue.astype(float),
        "COGS (R)": cogs_cost.astype(float),
        "OPEX (R)": opex.astype(float),
        "CAPEX (R)": capex.astype(float),
        "Net Cashflow (R)": net.astype(float)
    })
    return df

def recompute_from_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Revenue (R)"] = df["Units"] * df["Price (R/u)"]
    df["COGS (R)"] = df["Units"] * df["COGS (R/u)"]
    df["Net Cashflow (R)"] = df["Revenue (R)"] - df["COGS (R)"] - df["OPEX (R)"] - df["CAPEX (R)"]
    return df

def npv(rate: float, flows: list[float]) -> float:
    return float(np.sum([cf / (1.0 + rate)**t for t, cf in enumerate(flows, start=1)]))

def irr_bisection(flows_with_y0: list[float], lo: float = -0.99, hi: float = 5.0, tol=1e-6, max_iter=200):
    def f(r):
        return sum(cf / ((1 + r) ** t) for t, cf in enumerate(flows_with_y0, start=0))
    f_lo, f_hi = f(lo), f(hi)
    if np.isnan(f_lo) or np.isnan(f_hi) or f_lo * f_hi > 0:
        return np.nan
    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        f_mid = f(mid)
        if abs(f_mid) < tol:
            return mid
        if f_lo * f_mid < 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return np.nan

def payback_period(flows_with_y0: list[float]):
    cum = np.cumsum(flows_with_y0)
    for i in range(1, len(flows_with_y0)):
        if cum[i] >= 0:
            prev = cum[i-1]
            delta = flows_with_y0[i]
            if delta == 0:
                return float(i)
            frac = 1.0 - (prev / delta)
            return float(i - 1 + frac)
    return None

def scenario_metrics(df: pd.DataFrame, discount: float) -> dict:
    flows = df["Net Cashflow (R)"].tolist()
    irr_val = irr_bisection([0.0] + flows)
    return {
        "npv": npv(discount, flows),
        "irr": irr_val,
        "payback": payback_period([0.0] + flows),
        "pi": (npv(discount, flows) / max(1.0, float(df["CAPEX (R)"].sum())))
    }

def success_probability(df: pd.DataFrame, discount: float, n_sims: int) -> float:
    """
    Lightweight Monte Carlo: vary revenue, costs, and growth around current table values.
    For simplicity, apply random multipliers per year consistently within each simulation.
    """
    flows_base = df["Net Cashflow (R)"].to_numpy()
    rev_base = df["Revenue (R)"].to_numpy()
    cost_base = (df["COGS (R)"] + df["OPEX (R)"] + df["CAPEX (R)"]).to_numpy()

    success = 0
    rng = np.random.default_rng()
    for _ in range(n_sims):
        # Variation ranges (tweak as needed)
        rev_mult = rng.uniform(0.80, 1.20)    # ±20% revenue
        cost_mult = rng.uniform(0.85, 1.15)   # ±15% costs
        rate_mult = rng.uniform(0.90, 1.10)   # ±10% discount

        sim_rev = rev_base * rev_mult
        sim_cost = cost_base * cost_mult
        sim_flows = sim_rev - sim_cost
        if npv(discount * rate_mult, sim_flows.tolist()) > 0:
            success += 1
    return (success / n_sims) * 100.0

def apply_scenario(df: pd.DataFrame, kind: str, rev_up=0.20, cost_down=0.10, rev_down=0.20, cost_up=0.10) -> pd.DataFrame:
    df = df.copy()
    if kind == "optimistic":
        df["Price (R/u)"] *= (1.0 + rev_up)
        df["COGS (R/u)"] *= (1.0 - cost_down)
    elif kind == "pessimistic":
        df["Price (R/u)"] *= (1.0 - rev_down)
        df["COGS (R/u)"] *= (1.0 + cost_up)
    # Recompute revenue/COGS/net
    return recompute_from_columns(df)

# =============================
# Build Baseline DF
# =============================
units_vec = make_units_vector(units_y1, annual_units_growth, years)
baseline_df_default = build_df_from_units(units_vec, price, cogs, opex_fixed, capex_y1)
optimistic_df_default = apply_scenario(baseline_df_default, "optimistic", rev_up, cost_down, rev_down, cost_up)
pessimistic_df_default = apply_scenario(baseline_df_default, "pessimistic", rev_up, cost_down, rev_down, cost_up)

# Keep editable copies in session_state (one per scenario)
if "df_baseline" not in st.session_state:
    st.session_state.df_baseline = baseline_df_default.copy()
if "df_optimistic" not in st.session_state:
    st.session_state.df_optimistic = optimistic_df_default.copy()
if "df_pessimistic" not in st.session_state:
    st.session_state.df_pessimistic = pessimistic_df_default.copy()

# If years changed -> rebuild defaults & replace session copies to keep shapes aligned
for key, default_df in [
    ("df_baseline", baseline_df_default),
    ("df_optimistic", optimistic_df_default),
    ("df_pessimistic", pessimistic_df_default),
]:
    if len(st.session_state[key]) != years:
        st.session_state[key] = default_df.copy()

# =============================
# Tabs UI
# =============================
tabs = st.tabs(["Baseline", "Optimistic", "Pessimistic", "Summary"])

def scenario_tab(label: str, key: str, default_df: pd.DataFrame):
    st.markdown(f"### {label} Scenario")
    c1, c2, c3 = st.columns([1,1,2])
    with c1:
        if st.button("🔄 Refill from assumptions", key=f"refill_{key}"):
            st.session_state[key] = default_df.copy()
    with c2:
        if st.button("♻️ Reset (zeros except Year 1 CAPEX)", key=f"reset_{key}"):
            df = st.session_state[key].copy()
            df["Units"] = 0
            df["Price (R/u)"] = 0.0
            df["COGS (R/u)"] = 0.0
            df["Revenue (R)"] = 0.0
            df["COGS (R)"] = 0.0
            df["OPEX (R)"] = 0.0
            df["CAPEX (R)"] = 0.0
            df.loc[df.index[0], "CAPEX (R)"] = capex_y1
            df["Net Cashflow (R)"] = -df["CAPEX (R)"]
            st.session_state[key] = df

    st.caption("Edit any values directly. Net Cashflow updates when you change Units/Price/COGS/OPEX/CAPEX.")
    edited = st.data_editor(
        st.session_state[key],
        num_rows="fixed",
        use_container_width=True,
        hide_index=True
    )
    edited = recompute_from_columns(edited)

    # Persist
    st.session_state[key] = edited.copy()

    # Metrics
    mets = scenario_metrics(edited, discount)
    success_prob = success_probability(edited, discount, n_sims)

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("NPV (R)", f"{mets['npv']:,.0f}")
    m2.metric("IRR (%)", f"{(mets['irr']*100 if not np.isnan(mets['irr']) else 0):.1f}")
    m3.metric("Payback (yrs)", f"{mets['payback']:.1f}" if mets['payback'] is not None else "—")
    m4.metric("Profitability Index", f"{mets['pi']:,.2f}")
    m5.metric("Success Prob. (%)", f"{success_prob:.1f}")

    with st.expander("🧠 What this means (mentor tips)"):
        tips = []
        irr_val = mets['irr']
        if np.isnan(irr_val) or irr_val < 0.08:
            tips.append("⚠️ **IRR < 8%** — may struggle to attract investors; improve margins or reduce CAPEX.")
        elif irr_val < 0.15:
            tips.append("ℹ️ **IRR 8–15%** — borderline for commercial funds; blended finance may help.")
        else:
            tips.append("🚀 **IRR > 15%** — attractive for many investors.")
        if mets['payback'] is None or (mets['payback'] and mets['payback'] > 10):
            tips.append("⏳ **Payback > 10 years** — high risk; consider phasing CAPEX or performance-based models.")
        elif 5 < (mets['payback'] or 100) <= 10:
            tips.append("🕐 **Payback 5–10 years** — acceptable in infra/ESCO contexts.")
        else:
            tips.append("✅ **Payback < 5 years** — investor-friendly.")
        tips.append(f"🎯 **Success probability {success_prob:.0f}%** — based on {n_sims} runs with realistic uncertainty.")
        for t in tips:
            st.markdown("- " + t)

    return edited, mets, success_prob

with tabs[0]:
    df_base, base_mets, base_prob = scenario_tab("Baseline", "df_baseline", baseline_df_default)

with tabs[1]:
    df_opt, opt_mets, opt_prob = scenario_tab("Optimistic", "df_optimistic", optimistic_df_default)

with tabs[2]:
    df_pes, pes_mets, pes_prob = scenario_tab("Pessimistic", "df_pessimistic", pessimistic_df_default)

# =============================
# Summary tab
# =============================
with tabs[3]:
    st.markdown("### 📊 Scenario Summary")
    summary_df = pd.DataFrame([
        {"Scenario": "Baseline", "NPV (R)": base_mets["npv"], "IRR (%)": (base_mets["irr"]*100 if not np.isnan(base_mets["irr"]) else np.nan),
         "Payback (yrs)": base_mets["payback"], "PI": base_mets["pi"], "Success Prob. (%)": base_prob},
        {"Scenario": "Optimistic", "NPV (R)": opt_mets["npv"], "IRR (%)": (opt_mets["irr"]*100 if not np.isnan(opt_mets["irr"]) else np.nan),
         "Payback (yrs)": opt_mets["payback"], "PI": opt_mets["pi"], "Success Prob. (%)": opt_prob},
        {"Scenario": "Pessimistic", "NPV (R)": pes_mets["npv"], "IRR (%)": (pes_mets["irr"]*100 if not np.isnan(pes_mets["irr"]) else np.nan),
         "Payback (yrs)": pes_mets["payback"], "PI": pes_mets["pi"], "Success Prob. (%)": pes_prob},
    ])
    st.dataframe(summary_df.style.format({
        "NPV (R)": "{:,.0f}",
        "IRR (%)": "{:.1f}",
        "Payback (yrs)": "{:.1f}",
        "PI": "{:.2f}",
        "Success Prob. (%)": "{:.1f}"
    }), use_container_width=True, hide_index=True)

    # ---------- PDF / HTML export ----------
    st.markdown("#### 📄 Export Summary")

    def build_summary_text() -> str:
        lines = []
        lines.append(f"Financial Projection Summary — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("")
        lines.append(f"Years: {years}, Discount rate: {discount*100:.1f}%")
        lines.append("")
        for row in summary_df.itertuples(index=False):
            lines.append(f"{row[0]}: NPV R{row[1]:,.0f} | IRR {row[2]:.1f}% | Payback {row[3] if row[3] is not None else '—'} yrs | PI {row[4]:.2f} | Success {row[5]:.1f}%")
        lines.append("")
        lines.append("Notes:")
        lines.append("• Success probability is based on 1,000-run sensitivity around current table values.")
        lines.append("• IRR is annualized; Payback is fractional years to breakeven.")
        return "\n".join(lines)

    # Try PDF via reportlab; fallback to HTML
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import cm

        def make_pdf_bytes() -> bytes:
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=A4)
            width, height = A4
            textobj = c.beginText(2*cm, height - 2*cm)
            textobj.setFont("Helvetica", 10)
            for line in build_summary_text().splitlines():
                textobj.textLine(line)
            c.drawText(textobj)
            c.showPage()
            c.save()
            return buf.getvalue()

        pdf_bytes = make_pdf_bytes()
        st.download_button(
            "⬇️ Download PDF Summary",
            data=pdf_bytes,
            file_name="financial_projection_summary.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception:
        # Fallback: simple HTML download
        html = f"""
        <html><body>
        <pre style="font-family:Inter,ui-sans-serif;white-space:pre-wrap">{build_summary_text()}</pre>
        </body></html>
        """
        st.download_button(
            "⬇️ Download Summary (HTML fallback)",
            data=html.encode("utf-8"),
            file_name="financial_projection_summary.html",
            mime="text/html",
            use_container_width=True
        )

    with st.expander("🧠 How to use this in a pitch / application"):
        st.markdown(
            """
- Lead with **Baseline**: show NPV, IRR, Payback, and **Success Probability**.
- Use **Optimistic** to demonstrate upside; use **Pessimistic** to show risk awareness.
- Tie back to your **Business Model** (subscription vs. ESCO/BOOT influences payback and success odds).
- Add **ask & use of funds** (what CAPEX covers; expected runway to breakeven).
            """
        )


