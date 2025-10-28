# utils/model_logic.py
import json, os

# Path for business model data
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "business_models.json")

def load_models():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Questionnaire: scalable up to 60+ models later
questions = [
    {"id": 1, "text": "Do you prefer recurring revenue streams (e.g., subscriptions, maintenance)?", "tag_yes": "recurring"},
    {"id": 2, "text": "Is your primary customer a business (B2B) rather than individual consumers?", "tag_yes": "B2B"},
    {"id": 3, "text": "Is your product or service highly capital-intensive to deliver?", "tag_yes": "high_capex"},
    {"id": 4, "text": "Do you plan to manufacture or build physical assets?", "tag_yes": "infrastructure"},
    {"id": 5, "text": "Do you want to license or franchise your technology to others?", "tag_yes": "IP"},
    {"id": 6, "text": "Would you prefer to partner with distributors or resellers instead of selling directly?", "tag_yes": "distribution"},
    {"id": 7, "text": "Do you expect customers to pay based on usage (per hour, kWh, API call, etc.)?", "tag_yes": "usage"},
    {"id": 8, "text": "Are you currently in an early-stage or research-focused project (TRL ≤ 4)?", "tag_yes": "early_stage"},
    {"id": 9, "text": "Does your business rely on services or consulting revenue initially?", "tag_yes": "services"},
    {"id": 10, "text": "Do you envision scaling globally through digital delivery or SaaS?", "tag_yes": "software"}
]

def score_models(selected_tags, models):
    scored = []
    for model in models:
        model_tags = set(model.get("tags", []))
        score = len(model_tags.intersection(selected_tags))
        scored.append({"model": model, "score": score})
    return sorted(scored, key=lambda x: x["score"], reverse=True)[:3]
