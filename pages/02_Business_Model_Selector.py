import streamlit as st
import json

# -------------------------------
# Load Data
# -------------------------------
with open("data/business_models.json", "r") as f:
    BUSINESS_MODELS = json.load(f)

with open("data/archetype_tags.json", "r") as f:
    ARCHETYPE_TAGS = json.load(f)


MATURITY_MAP = {
    "emerging": 0.3,
    "established": 0.6,
    "dominant": 1.0
}


# -------------------------------
# Scoring Function
# -------------------------------
def score_model(model, archetype_tags):
    tag_overlap = len(set(model["tags"]) & set(archetype_tags)) / len(model["tags"])
    maturity_w = MATURITY_MAP[model["maturity_level"]]
    success = model["success_score"]

    final_score = (0.5 * tag_overlap) + (0.3 * success) + (0.2 * maturity_w)
    return final_score


# -------------------------------
# State Init
# -------------------------------
if "archetype" not in st.session_state:
    st.session_state["archetype"] = None

if "secondary_done" not in st.session_state:
    st.session_state["secondary_done"] = False


# -------------------------------
# UI Step 1: Choose Archetype
# -------------------------------
st.title("Business Model Selector")

if st.session_state["archetype"] is None:
    st.subheader("1. Choose your Innovator Archetype")
    choice = st.radio(
        "Select the profile that best matches you:",
        list(ARCHETYPE_TAGS.keys())
    )

    if st.button("Continue"):
        st.session_state["archetype"] = choice
        st.rerun()

else:
    archetype = st.session_state["archetype"]
    st.success(f"Selected Archetype: **{archetype}**")

    archetype_tags = ARCHETYPE_TAGS[archetype]

    # -------------------------------
    # UI Step 2: Secondary Questions
    # -------------------------------
    if not st.session_state["secondary_done"]:
        st.subheader("2. Refine your profile")

        q1 = st.selectbox(
            "How fast do you want to commercialize?",
            ["Slow & Research-heavy", "Moderate", "Fast"]
        )

        q2 = st.selectbox(
            "Which is more important to you?",
            ["Recurring revenue", "Impact outcomes", "User scale", "Technology depth"]
        )

        q3 = st.selectbox(
            "What is your available startup capital?",
            ["Very low (< R50k)", "Medium", "High"]
        )

        if st.button("Generate Recommendations"):
            st.session_state["secondary_done"] = True
            st.session_state["q1"] = q1
            st.session_state["q2"] = q2
            st.session_state["q3"] = q3
            st.rerun()

    # -------------------------------
   # -------------------------------
# Step 3: Ranking
# -------------------------------
if st.session_state["secondary_done"]:
    st.subheader("3. Recommended Business Models")

    # ---- Score models ----
    results = []
    for model in BUSINESS_MODELS:
        score = score_model(model, archetype_tags)
        results.append((model, score))

    results = sorted(results, key=lambda x: x[1], reverse=True)
    top5 = results[:5]

    # -------------------------------
    # Display Top 5 WITH full explanation
    # -------------------------------
    st.markdown("## 🔥 Top 5 Best-Fit Models")

    for bm, score in top5:
        st.markdown(f"### {bm['name']} — **Score: {score:.2f}**")
        st.markdown(f"**Description:** {bm['description']}")
        st.markdown(
            f"**Fit Quality:** Shares {len(set(bm['tags']) & set(archetype_tags))} strategic traits with your archetype."
        )
        st.markdown(f"**Success Rate:** {int(bm['success_score'] * 100)}%")
        st.markdown(f"**Maturity:** {bm['maturity_level'].title()}")
        st.markdown("---")

    # -------------------------------
    # Full list of all models (unchanged)
    # -------------------------------
    with st.expander("See all 70 business models"):
        for bm in BUSINESS_MODELS:
            st.markdown(f"#### {bm['name']}")
            st.markdown(bm["description"])
            st.caption(f"Tags: {', '.join(bm['tags'])}")
