
import json, os
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def load_models():
    with open(os.path.join(DATA_DIR,"business_models.json"),"r",encoding="utf-8") as f:
        return json.load(f)

def trl_gate(models, trl_level:int):
    return [m for m in models if m.get("trl_min",1) <= trl_level]

def score_models(profile:dict, models:list):
    results = []
    for m in models:
        score = 0
        tags = set(m.get("tags",[]))
        if profile.get("wants_recurring") and ("recurring" in tags or "software" in tags):
            score += 20
        if profile.get("customer_type") == "enterprise" and ("enterprise" in tags or "B2B" in tags):
            score += 15
        if profile.get("customer_type") == "SME" and ("SME" in tags or "B2B" in tags):
            score += 10
        if profile.get("capex") == "low" and ("low_capex" in tags or "software" in tags):
            score += 15
        if profile.get("capex") == "high" and ("infrastructure" in tags or "IoT" in tags):
            score += 10
        if profile.get("partner_ready") and ("distribution" in tags or "B2B" in tags):
            score += 8
        results.append({"model": m, "score": score})
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:3]
