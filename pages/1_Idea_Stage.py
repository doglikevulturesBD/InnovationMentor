import streamlit as st

st.header("🌱 TRL (Technology Readiness Level) Calculator")
st.markdown("Answer the questions below to estimate your technology's readiness level (TRL).")

# Step 1 — Key questions
concept = st.radio("Has the basic scientific concept been observed and reported?", ["No", "Yes"])
proof = st.radio("Has the technology concept been formulated and proof-of-concept demonstrated?", ["No", "Yes"])
lab = st.radio("Has the technology been validated in a lab environment?", ["No", "Yes"])
relevant = st.radio("Has it been demonstrated in a relevant environment (pilot scale)?", ["No", "Yes"])
operational = st.radio("Has it been demonstrated in an operational environment (real-world scale)?", ["No", "Yes"])
commercial = st.radio("Is the system proven and in commercial use?", ["No", "Yes"])

# Step 2 — Determine TRL
trl = 1
if concept == "Yes": trl = 2
if proof == "Yes": trl = 3
if lab == "Yes": trl = 4
if relevant == "Yes": trl = 6
if operational == "Yes": trl = 7
if commercial == "Yes": trl = 9

# Step 3 — Output result
if st.button("Calculate TRL"):
    st.success(f"Your estimated TRL is **{trl}**")
    
    # Guidance text
    guidance = {
        1: "Basic principles observed — start literature review and concept exploration.",
        2: "Technology concept formulated — define research objectives and experiments.",
        3: "Proof-of-concept demonstrated — build and test lab prototypes.",
        4: "Lab validation complete — prepare pilot-scale experiments.",
        5: "Technology validated in relevant environment — refine system design.",
        6: "Prototype demonstrated in relevant environment — engage with partners.",
        7: "System prototype in operational environment — plan scale-up.",
        8: "System complete and qualified — prepare for commercial deployment.",
        9: "System proven in operational environment — full commercial readiness."
    }
    st.info(guidance.get(trl, ""))
