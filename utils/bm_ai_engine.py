def ai_scores_for_models(full_text: str, model_names: List[str]) -> Dict[str, float]:

    vectors = load_model_vectors()

    if not vectors:
        return {m: 0.0 for m in model_names}

    # Auto-detect dimension needed
    sample_vec = next(iter(vectors.values()))
    target_dim = len(sample_vec)

    # Embed user text with correct dim
    user_vec = embed_text(full_text)
    if user_vec is None:
        return {m: 0.0 for m in model_names}

    # Resize or regenerate embedding to dimension
    if user_vec.shape[0] != target_dim:
        h = abs(hash(full_text.strip()))
        rng = np.random.default_rng(seed=h % (2**32))
        user_vec = rng.normal(size=target_dim)

    scores = {}

    for model in model_names:
        mvec_list = vectors.get(model)
        if not mvec_list:
            scores[model] = 0.0
            continue

        mvec = np.array(mvec_list)

        # Skip mismatched vectors
        if user_vec.shape[0] != mvec.shape[0]:
            scores[model] = 0.0
            continue

        dot = np.dot(user_vec, mvec)
        denom = (np.linalg.norm(user_vec) * np.linalg.norm(mvec))

        sim = float(dot / denom) if denom != 0 else 0.0
        scores[model] = sim

    # Normalise to 0–100
    vals = list(scores.values())
    vmin, vmax = min(vals), max(vals)

    if vmax == vmin:
        return {m: 0.0 for m in model_names}

    return {
        m: 100 * (s - vmin) / (vmax - vmin)
        for m, s in scores.items()
    }
