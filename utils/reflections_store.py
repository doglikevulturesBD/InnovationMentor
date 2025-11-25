import json
import streamlit as st
from datetime import datetime
import os

REFLECTION_FILE = "reflections.json"

def load_reflections():
    if not os.path.exists(REFLECTION_FILE):
        return []
    with open(REFLECTION_FILE, "r") as f:
        return json.load(f)

def save_reflection(module_name, reflection_text):
    reflections = load_reflections()

    entry = {
        "module": module_name,
        "reflection": reflection_text,
        "timestamp": datetime.now().isoformat()
    }

    reflections.append(entry)
    with open(REFLECTION_FILE, "w") as f:
        json.dump(reflections, f, indent=4)

def get_reflections_for_module(module_name):
    reflections = load_reflections()
    return [r for r in reflections if r["module"] == module_name]

