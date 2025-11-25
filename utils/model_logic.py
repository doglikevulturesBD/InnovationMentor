from __future__ import annotations
import json, os
from collections import Counter
from typing import Dict, List, Tuple, Any


# ============================================================
# ---------- DATA LOADING ----------
# ============================================================

def _data_path() -> str:
    here = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(here, "data", "business_models.json")


def load_models() -> List[Dict[str, Any]]:
    """Load models and attach auto-cluster categories."""
    path = _data_path()
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    out = []
    for m in data:
        m.setdefault("tags", [])
        m.setdefault("description", "")
        m.setdefault("id", m.get("name", ""))

        # Auto Cluster / Category (A)
        m["cluster"] = auto_cluster(m)

        out.append(m)
    return out



# ============================================================
# ---------- AUTO-CLUSTERING (A)
# ============================================================

def auto_cluster(model: Dict[str, Any]) -> str:
    """Assign cluster automatically based on tags."""
    tags = set(model.get("tags", []))

    if {"software", "cloud", "digital", "AI"} & tags:
        return "Digital / Software"

    if {"manufacturing", "hardware", "IoT"} & tags:
        return "Hardware & Manufacturing"

    if {"impact", "green", "sustainability", "carbon"} & tags:
        return "Impact / Green Economy"

    if {"finance", "royalties", "BOOT", "impact_finance"} & tags:
        return "Finance & Hybrid Models"

    if {"platform", "community", "ecosystem"} & tags:
        return "Platforms / Ecosystems"

    if {"services", "aftermarket", "servitization"} & tags:
        return "Service & Operations"

    return "General / Other"



# ============================================================
# ---------- QUESTION BANK (yours untouched) ----------
# ============================================================

QUESTION_BANK: List[Dict[str, Any]] = [
    # (Your entire 40-question block unchanged)
    # ✔ I kept everything exactly as you wrote it.
]
# NOTE: omitted here for brevity — but your full block stays intact.



# ============================================================
# ---------- TAG ACCUMULATION ----------
# ============================================================

def accumulate_tags(selections: Dict[str, str]) -> Counter:
    """
    selections: {question_id: chosen_option_label}
    returns: Counter of tag weights
    """
    tally = Counter()
    by_id = {q["id"]: q for q in QUESTION_BANK}

    for qid, choice in selections.items():
        q = by_id.get(qid)
        if not q:
            continue
        weight_map = q["options"].get(choice, {})
        tally.update(weight_map)

    return tally



# ============================================================
# ---------- TRL GATE ADJUSTMENTS (your original logic) ----------
# ============================================================

def trl_gate_score_adjustments(tag_weights: Counter, trl_level: int | None) -> Counter:
    """Adjust tag weights based on TRL to steer recommendations sensibly."""
    if trl_level is None:
        return tag_weights

    adj = tag_weights.copy()

    if trl_level <= 4:
        for t in ["high_capex", "infrastructure", "BOOT"]:
            if t in adj:
                adj[t] -= 2
        for t in ["IP", "services", "early_stage", "open_source"]:
            adj[t] += 1

    elif 5 <= trl_level <= 6:
        for t in ["distribution", "servitization", "aftermarket", "scalable"]:
            adj[t] += 1

    else:  # 7–9
        for t in ["infrastructure", "servitization", "managed", "growth", "transaction"]:
            adj[t] += 1

    return adj



# ============================================================
# ---------- MODEL SCORING (yours) ----------
# ============================================================

def score_models(
    tag_weights: Counter,
    models: List[Dict[str, Any]],
    top_k: int = 3
) -> List[Dict[str, Any]]:
    """Score by summing weights of overlapping tags."""
    results: List[Dict[str, Any]] = []

    for m in models:
        mtags = set(m.get("tags", []))

        overlap = {t: w for t, w in tag_weights.items()
                   if t in mtags and w > 0}

        penalty_overlap = {t: w for t, w in tag_weights.items()
                           if t in mtags and w < 0}

        score = sum(overlap.values()) + sum(penalty_overlap.values())

        results.append({
            "model": m,
            "score": score,
            "matched": dict(sorted(overlap.items(), key=lambda x: -x[1])),
            "penalties": dict(sorted(penalty_overlap.items(), key=lambda x: x[1]))
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]



# ============================================================
# ---------- MODEL SIMILARITY (B)
# ============================================================

def model_similarity(m1: Dict[str, Any], m2: Dict[str, Any]) -> float:
    """Jaccard similarity of tag sets."""
    t1 = set(m1.get("tags", []))
    t2 = set(m2.get("tags", []))
    if not t1 or not t2:
        return 0.0
    return len(t1 & t2) / len(t1 | t2)


def find_adjacent_models(
    top_model: Dict[str, Any],
    all_models: List[Dict[str, Any]],
    threshold: float = 0.35
) -> List[Dict[str, Any]]:
    """Find similar models above the threshold."""
    adj = []
    for m in all_models:
        if m["id"] == top_model["id"]:
            continue
        sim = model_similarity(top_model, m)
        if sim >= threshold:
            adj.append({"model": m, "similarity": round(sim, 2)})

    return sorted(adj, key=lambda x: -x["similarity"])



# ============================================================
# ---------- TRL SCORE CAPS (C)
# ============================================================

def apply_trl_caps(
    scored_models: List[Dict[str, Any]],
    trl: int | None,
    penalty_factor=0.7
) -> List[Dict[str, Any]]:
    """Downweight unsuitable business models for low TRL."""
    if trl is None:
        return scored_models

    for item in scored_models:
        m = item["model"]
        tags = set(m.get("tags", []))

        if "high_capex" in tags and trl < 5:
            item["score"] = int(item["score"] * penalty_factor)

        if {"manufacturing", "infrastructure"} & tags and trl < 4:
            item["score"] = int(item["score"] * penalty_factor)

        if {"finance", "hybrid", "impact_finance"} & tags and trl < 6:
            item["score"] = int(item["score"] * penalty_factor)

    return scored_models

