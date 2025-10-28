# utils/model_logic.py
from __future__ import annotations
import json, os
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Any

# ---------- DATA LOADING ----------
def _data_path() -> str:
    here = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(here, "data", "business_models.json")

def load_models() -> List[Dict[str, Any]]:
    path = _data_path()
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # normalize
    out = []
    for m in data:
        m.setdefault("tags", [])
        m.setdefault("description", "")
        m.setdefault("id", m.get("name", ""))
        out.append(m)
    return out

# ---------- QUESTION BANK (40) ----------
# Each question: id, section, text, options -> tag weights
# Weights are additive; higher = stronger preference.
QUESTION_BANK: List[Dict[str, Any]] = [
    # A. Offering & Delivery (1–6)
    {"id": "A1", "section": "Offering", "text": "What is your primary offering?",
     "options": {
         "Product (physical)": {"hardware": 2, "manufacturing": 2},
         "Service (people-delivered)": {"services": 2},
         "Digital / Software": {"software": 3, "platform": 1}
     }},
    {"id": "A2", "section": "Offering", "text": "How is the value primarily delivered?",
     "options": {
         "On-site / installed": {"infrastructure": 2},
         "Remote / digital": {"digital": 2},
         "Hybrid (physical + digital)": {"IoT": 2, "hybrid": 1}
     }},
    {"id": "A3", "section": "Offering", "text": "Does your product evolve with continuous updates?",
     "options": {"No": {}, "Yes, minor updates": {"aftermarket": 1}, "Yes, frequent updates": {"recurring": 2, "product_led": 1}}},
    {"id": "A4", "section": "Offering", "text": "Is data/analytics core to your value?",
     "options": {"No": {}, "Somewhat": {"data": 1}, "Yes, central": {"data": 2, "AI": 2}}},
    {"id": "A5", "section": "Offering", "text": "Will customers interact regularly (weekly+) with your solution?",
     "options": {"Rarely": {}, "Sometimes": {"engagement": 1}, "Frequently": {"engagement": 2, "growth": 1}}},
    {"id": "A6", "section": "Offering", "text": "Is your value proposition network/marketplace-based?",
     "options": {"No": {}, "Emerging": {"platform": 1}, "Yes": {"platform": 2, "transaction": 1}}},

    # B. Customer & Relationship (7–11)
    {"id": "B1", "section": "Customers", "text": "Primary customer?",
     "options": {"B2C": {"B2C": 2}, "SME": {"B2B": 2}, "Enterprise": {"enterprise": 2, "B2B": 1}, "Government": {"public": 2}}},
    {"id": "B2", "section": "Customers", "text": "Sales motion?",
     "options": {"Self-serve": {"product_led": 2}, "Inside sales": {"B2B": 1}, "Enterprise field sales": {"enterprise": 2}}},
    {"id": "B3", "section": "Customers", "text": "Will you rely on partners/resellers?",
     "options": {"No": {}, "Maybe later": {"distribution": 1}, "Yes, core channel": {"distribution": 2}}},
    {"id": "B4", "section": "Customers", "text": "Community/user-generated content important?",
     "options": {"No": {}, "Somewhat": {"community": 1}, "Yes": {"community": 2}}},
    {"id": "B5", "section": "Customers", "text": "Average contract length (if B2B)?",
     "options": {"One-off": {}, "1–12 months": {"recurring": 1}, "12+ months": {"recurring": 2, "managed": 1}}},

    # C. Revenue Logic (12–17)
    {"id": "C1", "section": "Revenue", "text": "Preferred revenue style?",
     "options": {"One-off sales": {"one_off": 2}, "Recurring (subscription/contract)": {"recurring": 3}, "Usage-based": {"usage": 3}}},
    {"id": "C2", "section": "Revenue", "text": "Licensing/royalties likely?",
     "options": {"No": {}, "Maybe": {"IP": 1}, "Yes": {"IP": 2, "royalties": 2}}},
    {"id": "C3", "section": "Revenue", "text": "Commission/brokerage opportunity?",
     "options": {"No": {}, "Some": {"transaction": 1}, "Yes": {"transaction": 2}}},
    {"id": "C4", "section": "Revenue", "text": "Monetizing data/insights?",
     "options": {"No": {}, "Possibly": {"data": 1}, "Core revenue": {"data": 2, "AI": 1}}},
    {"id": "C5", "section": "Revenue", "text": "Outcome/pay-for-performance alignment?",
     "options": {"No": {}, "Maybe": {"performance": 1}, "Yes": {"performance": 2}}},
    {"id": "C6", "section": "Revenue", "text": "Freemium or free tier?",
     "options": {"No": {}, "Maybe": {"freemium": 1}, "Yes": {"freemium": 2, "growth": 1}}},

    # D. Technology & IP (18–22)
    {"id": "D1", "section": "Technology & IP", "text": "Proprietary technology/IP central?",
     "options": {"No": {}, "Some": {"IP": 1}, "Yes": {"IP": 2}}},
    {"id": "D2", "section": "Technology & IP", "text": "Open APIs / interoperability?",
     "options": {"No": {}, "Some": {"developer": 1}, "Yes": {"developer": 2}}},
    {"id": "D3", "section": "Technology & IP", "text": "AI/automation core to product/process?",
     "options": {"No": {}, "Supporting": {"AI": 1}, "Core": {"AI": 2}}},
    {"id": "D4", "section": "Technology & IP", "text": "Open-source core strategy?",
     "options": {"No": {}, "Maybe": {"open_source": 1}, "Yes": {"open_source": 2}}},
    {"id": "D5", "section": "Technology & IP", "text": "Plan to franchise or standardize playbook?",
     "options": {"No": {}, "Maybe": {"franchise": 1}, "Yes": {"franchise": 2}}},

    # E. Capital & Risk (23–28)
    {"id": "E1", "section": "Capital & Risk", "text": "Capex intensity of delivery?",
     "options": {"Low": {"low_capex": 2}, "Medium": {"med_capex": 2}, "High": {"high_capex": 3}}},
    {"id": "E2", "section": "Capital & Risk", "text": "Consider BOOT/PPP concession type models?",
     "options": {"No": {}, "Maybe": {"BOOT": 1}, "Yes": {"BOOT": 2, "infrastructure": 1}}},
    {"id": "E3", "section": "Capital & Risk", "text": "Blend grants, equity, and loans?",
     "options": {"No": {}, "Maybe": {"blended": 1}, "Yes": {"blended": 2}}},
    {"id": "E4", "section": "Capital & Risk", "text": "Impact-linked loans/green bonds relevant?",
     "options": {"No": {}, "Some": {"impact_finance": 1}, "Yes": {"impact_finance": 2, "impact": 1}}},
    {"id": "E5", "section": "Capital & Risk", "text": "Scale without proportional capex increases?",
     "options": {"No": {}, "Somewhat": {"scalable": 1}, "Yes": {"scalable": 2}}},

    # F. Ops & Supply (29–33)
    {"id": "F1", "section": "Ops", "text": "Who makes the product?",
     "options": {"Outsource": {"white_label": 2}, "In-house": {"manufacturing": 2}, "Network/on-demand": {"digital_mfg": 2}}},
    {"id": "F2", "section": "Ops", "text": "Maintenance/servitization planned?",
     "options": {"No": {}, "Maybe": {"aftermarket": 1}, "Yes": {"aftermarket": 2, "servitization": 2}}},
    {"id": "F3", "section": "Ops", "text": "Circularity/second-life important?",
     "options": {"No": {}, "Some": {"circular": 1}, "Yes": {"circular": 2}}},
    {"id": "F4", "section": "Ops", "text": "Supply chain footprint?",
     "options": {"Local": {"local": 1}, "Global": {"global": 1}, "Hybrid": {"hybrid": 1}}},
    {"id": "F5", "section": "Ops", "text": "On-demand fabrication or 3D printing?",
     "options": {"No": {}, "Maybe": {"additive": 1}, "Yes": {"additive": 2, "digital_mfg": 1}}},

    # G. Innovation & Stage (34–37)
    {"id": "G1", "section": "Stage", "text": "Current TRL (1–9)?",
     "options": {"1–3": {"early_stage": 2}, "4–6": {"mid_stage": 2}, "7–9": {"late_stage": 2}}},
    {"id": "G2", "section": "Stage", "text": "Are you still in R&D/PoC?",
     "options": {"No": {}, "Partly": {"early_stage": 1}, "Yes": {"early_stage": 2}}},
    {"id": "G3", "section": "Stage", "text": "Preparing to scale/repeat in new markets?",
     "options": {"No": {}, "Soon": {"growth": 1}, "Yes": {"growth": 2}}},
    {"id": "G4", "section": "Stage", "text": "Would you join accelerators/partners for go-to-market?",
     "options": {"No": {}, "Maybe": {"partnerships": 1}, "Yes": {"partnerships": 2}}},

    # H. Impact & Ecosystem (38–40)
    {"id": "H1", "section": "Impact", "text": "Environmental/social impact central?",
     "options": {"No": {}, "Some": {"impact": 1}, "Yes": {"impact": 2}}},
    {"id": "H2", "section": "Impact", "text": "Monetize impact (credits/outcomes)?",
     "options": {"No": {}, "Maybe": {"impact_mon": 1}, "Yes": {"impact_mon": 2, "carbon": 1}}},
    {"id": "H3", "section": "Impact", "text": "Shared ownership/cooperative model?",
     "options": {"No": {}, "Maybe": {"cooperative": 1}, "Yes": {"cooperative": 2, "community": 1}}}
]

# ---------- TAG ACCUMULATION ----------
def accumulate_tags(selections: Dict[str, str]) -> Counter:
    """
    selections: {question_id: chosen_option_label}
    returns: Counter of tag weights
    """
    tally = Counter()
    by_id = {q["id"]: q for q in QUESTION_BANK}
    for qid, choice in selections.items():
        q = by_id.get(qid)
        if not q: continue
        weight_map = q["options"].get(choice, {})
        tally.update(weight_map)
    return tally

# ---------- TRL GATE / ADJUSTMENTS ----------
def trl_gate_score_adjustments(tag_weights: Counter, trl_level: int | None) -> Counter:
    """
    Adjust tag weights based on TRL to steer recommendations sensibly.
    """
    if trl_level is None:
        return tag_weights

    adj = tag_weights.copy()
    if trl_level <= 4:
        # Early: discourage heavy capex & concessions
        for t in ["high_capex", "infrastructure", "BOOT"]:
            if t in adj: adj[t] -= 2
        # Encourage IP/licensing, consulting, grants
        for t in ["IP", "services", "early_stage", "open_source"]:
            adj[t] += 1
    elif 5 <= trl_level <= 6:
        # Mid: neutral, slight boost for channels/servitization
        for t in ["distribution", "servitization", "aftermarket", "scalable"]:
            adj[t] += 1
    else:  # 7–9
        # Late: boost infrastructure/servitization/managed
        for t in ["infrastructure", "servitization", "managed", "growth", "transaction"]:
            adj[t] += 1
    return adj

# ---------- MODEL SCORING ----------
def score_models(tag_weights: Counter, models: List[Dict[str, Any]], top_k: int = 3
                 ) -> List[Dict[str, Any]]:
    """
    Score by summing weights of overlapping tags.
    Returns list sorted desc by score with rationale.
    """
    results: List[Dict[str, Any]] = []
    for m in models:
        mtags = set(m.get("tags", []))
        overlap = {t: w for t, w in tag_weights.items() if t in mtags and w > 0}
        penalty_overlap = {t: w for t, w in tag_weights.items() if t in mtags and w < 0}
        score = sum(overlap.values()) + sum(penalty_overlap.values())
        results.append({
            "model": m,
            "score": score,
            "matched": dict(sorted(overlap.items(), key=lambda x: -x[1])),
            "penalties": dict(sorted(penalty_overlap.items(), key=lambda x: x[1]))
        })
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]
