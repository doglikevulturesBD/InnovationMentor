import streamlit as st
from utils.data_loader import (
    load_business_models,
    load_archetype_questions,
    load_archetypes,
    load_secondary_questions,
)

st.set_page_config(page_title="Business Model Guide", layout="wide")

st.title("Innovation Mentor — Business Model Guide")

# --- Load data ---
business_models = load_business_models()
questions = load_archetype_questions()
archetypes = load_archetypes()
secondary_q = load_secondary_questions()

# --- Stage 1: Archetype questions ---
st.header("Step 1 — Your Strategic Fingerprint")

answers = {}

for q in questions:
    answers[q["key"]] = st.selectbox(
        q["text"],
        q["options"],
        key=f"arch_{q['id']}"
    )

st.write("Raw answers (for debugging):", answers)

# --- Simple heuristic: guess primary archetype based on answers ---
def infer_archetype(answers_dict):
    """
    Very simple rule-based mapping for now.
    Later we can replace this with a nicer scoring system.
    """
    score = {a["id"]: 0 for a in archetypes}

    # Delivery style (Q1)
    delivery = answers_dict.get("delivery", "").lower()
    if "software" in delivery or "hybrid" in delivery:
        score["A_SOFTWARE"] += 2
    if "platform" in delivery:
        score["A_PLATFORM"] += 2
    if "product" in delivery or "hybrid" in delivery:
        score["A_HARDWARE"] += 1
    if "service" in delivery:
        score["A_IMPACT"] += 0.5  # could also map to services later

    # Scale (Q2)
    scale = answers_dict.get("scale", "").lower()
    if "digital" in scale or "ecosystem" in scale or "international" in scale:
        score["A_SOFTWARE"] += 1
        score["A_PLATFORM"] += 1
    if "local" in scale or "national" in scale:
        score["A_IMPACT"] += 0.5
        score["A_HARDWARE"] += 0.5

    # Revenue preference (Q4)
    revenue = answers_dict.get("revenue", "").lower()
    if "licensing" in revenue:
        score["A_SOFTWARE"] += 1
        score["A_FINANCE"] += 0.5
    if "marketplace" in revenue:
        score["A_PLATFORM"] += 1.5
    if "usage" in revenue:
        score["A_SOFTWARE"] += 0.5
        score["A_HARDWARE"] += 0.5
        score["A_FINANCE"] += 0.5

    # R&D intensity (Q5)
    rnd = answers_dict.get("rnd_intensity", "").lower()
    if "high" in rnd or "deep" in rnd:
        score["A_SOFTWARE"] += 0.5
        score["A_IMPACT"] += 0.5
        score["A_HARDWARE"] += 0.5

    # Regulation (Q8)
    reg = answers_dict.get("regulation", "").lower()
    if "high" in reg or "extreme" in reg:
        score["A_IMPACT"] += 1
        score["A_FINANCE"] += 1

    # pick best
    best_id = max(score, key=score.get)
    best = next(a for a in archetypes if a["id"] == best_id)
    return best, score

if st.button("Analyse my archetype"):
    primary, scores = infer_archetype(answers)
    st.subheader("Your primary archetype")
    st.markdown(f"**{primary['name']}**")
    st.write(primary["description"])
    st.write("Debug scores:", scores)

    # --- Stage 2: Show secondary questions for that archetype ---
    st.header("Step 2 — Fine-tune within this archetype")

    sec_set = secondary_q.get(primary["id"], [])
    sec_answers = {}
    for q in sec_set:
        sec_answers[q["id"]] = st.selectbox(
            q["text"],
            q["options"],
            key=f"sec_{q['id']}"
        )

    st.write("Secondary answers (debug):", sec_answers)

    # --- Stage 3: Show matching business models list (first version: just filter by tags) ---
    st.header("Recommended business models in this space")

    core_tags = set(primary["core_tags"])

    # simple score: overlap of core_tags with BM tags
    scored = []
    for bm in business_models:
        overlap = core_tags.intersection(set(bm["tags"]))
        score = len(overlap)
        scored.append((score, bm))

    # sort by score desc
    scored.sort(key=lambda x: x[0], reverse=True)

    top_models = [bm for s, bm in scored if s > 0]

    if not top_models:
        st.info("No strong matches yet — your archetype is quite niche. We can later improve the mapping.")
    else:
        st.markdown("These are the **closest fits** based on your archetype. You can read them all and then pick your Top 3.")

        names_for_multiselect = [f"{bm['id']} — {bm['name']}" for bm in top_models]

        chosen = st.multiselect(
            "Choose up to 3 models that feel right for your innovation:",
            options=names_for_multiselect,
            max_selections=3
        )

        # show details for all models
        for score_val, bm in scored:
            if score_val <= 0:
                continue
            with st.expander(f"{bm['id']} — {bm['name']}"):
                st.write(bm["description"])
                st.write("Tags:", ", ".join(bm["tags"]))
                st.caption(f"Archetype match score (rough): {score_val}")

        if chosen:
            st.success("Saved your Top 3 choices.")
            st.session_state["top3_models"] = chosen
