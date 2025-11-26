import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # points to innovation_mentor/

def load_json(relative_path: str):
    full_path = BASE_DIR / relative_path
    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_business_models():
    return load_json("data/business_models.json")

def load_archetype_questions():
    return load_json("data/archetype_questions.json")

def load_archetypes():
    return load_json("data/archetypes.json")

def load_secondary_questions():
    return load_json("data/secondary_questions.json")
