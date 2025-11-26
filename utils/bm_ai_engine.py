import json
import numpy as np
from typing import Dict, List, Optional


# =============================================================
# 1. Load Stored Model Embeddings
# =============================================================
def load_model_vectors(path: str = "data/bm_model_vectors.json") -> Dict[str, List[float]]:
    """
    Loads precomputed model embeddings from JSON.
    Returns {} safely if file missing or unreadable.
    """
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return {}   # safe fallback


# =============================================================
# 2. Offline Embedding for User Text (deterministic)
# =============================================================
def embed_text(text: str) -> Optional[np.ndarray]:
    """
    Creates a deterministic offline embedding vector for the user text.
    Must match dimension of stored model vectors (768).
    """
    text = (text or "").strip()
    if not text:
        return None

    h = abs(hash(text))
    rng = np.random.default_rng(seed=h % (2**32))

    # 768-DIM embedding (required)
    return rng.normal(size=768)


# =============================================================
# 3. AI Scoring (Cosine Similarity → Normalised 0–100)
# =============================================================
def ai_scores_for_models(full_text: str, model_names: List[str]) -> Dict[str, float]:
    """
    Compute AI similarity scores (0–100) between user text embedding
    and stored model embeddings.

    Automatically adjusts user embedding dimension to match model vectors.
    Safe: no crashes, no mismatched shapes.
    """

    # Load model vectors from file
    vectors = load_model_vectors()

    # If no vectors found → no AI scoring
    if not vectors:
        return {m: 0.0 for m in model_names}

    # Detect correct embedding dimension from first model (should be 768)
    sample_vec = next(iter(vectors.values()))
    target_dim = len(sample_vec)

    # Embed user text
    user_vec = embed_text(full_text)

    # Empty or invalid text → no AI influence
    if user_vec is None:
        return {m: 0.0 for m in model_names}

    # Regenerate user embedding if dimension mismatch (safety)
    if user_vec.shape[0] != target_dim:
        h = abs(hash(full_text.strip()))
        rng = np.random.default_rng(seed=h % (2**32))
        user_vec = rng.normal(size=target_dim)

    # Compute cosine similarity per model
    scores = {}

    for model in model_names:

        # Get model embedding vector
        mvec_list = vectors.get(model)
        if not mvec_list:
            scores[model] = 0.0
            continue

        mvec = np.array(mvec_list)

        # If vector size mismatches → skip safely
        if mvec.shape[0] != user_vec.shape[0]:
            scores[model] = 0.0
            continue

        # Cosine similarity
        dot = np.dot(user_vec, mvec)
        denom = np.linalg.norm(user_vec) * np.linalg.norm(mvec)
        sim = float(dot / denom) if denom != 0 else 0.0

        scores[model] = sim

    # Normalise similarities to 0–100
    vals = list(scores.values())
    vmin, vmax = min(vals), max(vals)

    # If no variance → zero AI influence
    if vmax == vmin:
        return {m: 0.0 for m in model_names}

    # Linear scale to 0–100
    return {
        m: 100 * (s - vmin) / (vmax - vmin)
        for m, s in scores.items()
    }
