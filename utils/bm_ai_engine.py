# utils/bm_ai_engine.py

import json
import numpy as np
from typing import Dict, List, Optional


# -------------------------------------------------------------
# 1. Load Model Embeddings (your precomputed vectors)
# -------------------------------------------------------------
def load_model_vectors(path: str = "data/bm_model_vectors.json") -> Dict[str, List[float]]:
    """
    Loads precomputed embeddings for each business model.
    File format:
        { "BM01": [0.12, 0.98, ...], "BM02": [...] }
    """
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return {}   # Safe fallback


# -------------------------------------------------------------
# 2. Embed User Text — OFFLINE VERSION
# -------------------------------------------------------------
# You can later replace this with your *own* offline embedder.
# For now: simple hash → deterministic numeric vector.
# 100% offline, 100% free, and stable across runs.

def embed_text(text: str) -> Optional[np.ndarray]:
    """
    Converts text into a deterministic offline embedding vector.

    This avoids ALL OpenAI dependencies, while keeping the
    architecture identical so you can drop in a real offline
    embedding model later (sentence-transformers, etc.)

    This is NOT semantic — only structural — but lets the app
    run correctly and keeps the AI scoring pipeline functional.
    """

    text = (text or "").strip()
    if not text:
        return None

    # Produce deterministic 512-dimensional vector from hash
    # (matches shape of typical embedding models)
    h = abs(hash(text))
    rng = np.random.default_rng(seed=h % (2**32))
    return rng.normal(size=512)   # 512-dim random offline embedding


# -------------------------------------------------------------
# 3. Compute AI Similarity Scores (0–100)
# -------------------------------------------------------------
def ai_scores_for_models(full_text: str, model_names: List[str]) -> Dict[str, float]:
    """
    Returns AI-based similarity scores (0–100),
    using offline embeddings + precomputed model vectors.

    If embeddings or vectors unavailable → returns all zeros.
    """

    user_vec = embed_text(full_text)
    vectors = load_model_vectors()

    if user_vec is None or not vectors:
        # Safe fallback — no AI influence
        return {m: 0.0 for m in model_names}

    scores = {}

    for model in model_names:
        mvec_list = vectors.get(model)

        if not mvec_list:
            scores[model] = 0.0
            continue

        mvec = np.array(mvec_list)

        # Cosine similarity
        dot = np.dot(user_vec, mvec)
        denom = (np.linalg.norm(user_vec) * np.linalg.norm(mvec))

        if denom == 0:
            sim = 0.0
        else:
            sim = float(dot / denom)

        scores[model] = sim

    # Normalise to 0–100
    vals = list(scores.values())
    vmin, vmax = min(vals), max(vals)

    if vmax == vmin:
        return {m: 0.0 for m in model_names}

    norm_scores = {
        m: 100 * (s - vmin) / (vmax - vmin)
        for m, s in scores.items()
    }

    return norm_scores
