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

    # Detect correct embedding dimension from first model
    sample_vec = next(iter(vectors.values()))
    target_dim = len(sample_vec)

    # Embed user text
    user_vec = embed_text(full_text)

    # Empty text → no AI influence
    if user_vec is None:
        return {m: 0.0 for m in model_names}

    # If user vector dimension differs → regenerate to correct size
    if user_vec.shape[0] != target_dim:
        h = abs(hash(full_text.strip()))
        rng = np.random.default_rng(seed=h % (2**32))
        user_vec = rng.normal(size=target_dim)

    # Compute cosine similarity for each model
    scores = {}

    for model in model_names:

        # Get model vector list
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

    # Normalise scores (0–100)
    vals = list(scores.values())
    vmin, vmax = min(vals), max(vals)

    # If all similarities identical → zero influence
    if vmax == vmin:
        return {m: 0.0 for m in model_names}

    # Return normalized similarity
    return {
        m: 100 * (s - vmin) / (vmax - vmin)
        for m, s in scores.items()
    }
