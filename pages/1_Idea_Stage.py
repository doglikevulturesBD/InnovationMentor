import streamlit as st

st.header("🌱 TRL (Technology Readiness Level) Calculator")
st.markdown("""
Answer the questions in order to find your technology's current readiness level (TRL).
The next question will only appear once you select **Yes** on the current stage.
""")

trl = 1
stage = ""

# Stage 1
q1 = st.radio("🔹 TRL 1 — Have the basic scientific principles been observed and reported?", ["No", "Yes"], index=0)
if q1 == "Yes":
    trl = 2
    stage = "Basic principles observed"
    
    # Stage 2
    q2 = st.radio("🔹 TRL 2 — Has the technology concept been formulated?", ["No", "Yes"], index=0)
    if q2 == "Yes":
        trl = 3
        stage = "Technology concept formulated"
        
        # Stage 3
        q3 = st.radio("🔹 TRL 3 — Has proof-of-concept been demonstrated?", ["No", "Yes"], index=0)
        if q3 == "Yes":
            trl = 4
            stage = "Proof-of-concept demonstrated"
            
            # Stage 4
            q4 = st.radio("🔹 TRL 4 — Has the technology been validated in a lab environment?", ["No", "Yes"], index=0)
            if q4 == "Yes":
                trl = 5
                stage = "Lab validation complete"
                
                # Stage 5
                q5 = st.radio("🔹 TRL 5 — Has the technology been validated in a relevant environment (pilot scale)?", ["No", "Yes"], index=0)
                if q5 == "Yes":
                    trl = 6
                    stage = "Validated in relevant environment"
                    
                    # Stage 6
                    q6 = st.radio("🔹 TRL 6 — Has it been demonstrated in a relevant environment?", ["No", "Yes"], index=0)
                    if q6 == "Yes":
                        trl = 7
                        stage = "Demonstrated in relevant environment"
                        
                        # Stage 7
                        q7 = st.radio("🔹 TRL 7 — Has it been demonstrated in an operational environment (real-world)?", ["No", "Yes"], index=0)
                        if q7 == "Yes":
                            trl = 8
                            stage = "Operational demonstration"
                            
                            # Stage 8
                            q8 = st.radio("🔹 TRL 8 — Has the system been qualified and ready for commercial deployment?", ["No", "Yes"], index=0)
                            if q8 == "Yes":
                                trl = 9
                                stage = "System proven in operational environment"

if st.button("Show My TRL"):
    st.success(f"Your estimated TRL is **{trl}** — {stage if stage else 'Basic principles observed'}")

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
