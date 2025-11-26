import json
from pathlib import Path

# ------------------------------
# 1. Define your evidence-based mappings
# ------------------------------

DOMINANT = 0.90
ESTABLISHED = 0.75
EMERGING = 0.55

MAPPINGS = {
    # DOMINANT
    "BM01": DOMINANT, "BM03": DOMINANT, "BM06": DOMINANT, "BM07": DOMINANT,
    "BM08": DOMINANT, "BM09": DOMINANT, "BM10": DOMINANT, "BM11": DOMINANT,
    "BM12": DOMINANT, "BM20": DOMINANT, "BM21": DOMINANT, "BM22": DOMINANT,
    "BM23": DOMINANT, "BM25": DOMINANT, "BM36": DOMINANT, "BM37": DOMINANT,
    "BM42": DOMINANT, "BM60": DOMINANT,

    # ESTABLISHED
    "BM02": ESTABLISHED, "BM04": ESTABLISHED, "BM05": ESTABLISHED,
    "BM13": ESTABLISHED, "BM14": ESTABLISHED, "BM15": ESTABLISHED,
    "BM16": ESTABLISHED, "BM17": ESTABLISHED, "BM18": ESTABLISHED,
    "BM19": ESTABLISHED, "BM24": ESTABLISHED, "BM26": ESTABLISHED,
    "BM27": ESTABLISHED, "BM28": ESTABLISHED, "BM29": ESTABLISHED,
    "BM30": ESTABLISHED, "BM31": ESTABLISHED, "BM32": ESTABLISHED,
    "BM39": ESTABLISHED, "BM40": ESTABLISHED, "BM41": ESTABLISHED,
    "BM43": ESTABLISHED, "BM44": ESTABLISHED, "BM45": ESTABLISHED,
    "BM46": ESTABLISHED, "BM47": ESTABLISHED, "BM48": ESTABLISHED,
    "BM49": ESTABLISHED, "BM50": ESTABLISHED, "BM51": ESTABLISHED,
    "BM52": ESTABLISHED, "BM53": ESTABLISHED, "BM55": ESTABLISHED,
    "BM56": ESTABLISHED, "BM57": ESTABLISHED,

    # EMERGING
    "BM33": EMERGING, "BM34": EMERGING, "BM35": EMERGING, "BM38": EMERGING,
    "BM54": EMERGING, "BM58": EMERGING, "BM61": EMERGING, "BM62": EMERGING,
    "BM63": EMERGING, "BM64": EMERGING, "BM65": EMERGING, "BM66": EMERGING,
    "BM67": EMERGING, "BM68": EMERGING, "BM69": EMERGING, "BM70": EMERGING
}


# ------------------------------
# 2. Convert score → human-readable maturity band
# ------------------------------
def score_to_maturity(score):
    if score == DOMINANT:
        return "dominant"
    if score == ESTABLISHED:
        return "established"
    if score == EMERGING:
        return "emerging"
    return "unknown"


# ------------------------------
# 3. Load, enrich, save
# ------------------------------
def enrich_models():
    base_path = Path(__file__).resolve().parent.parent / "data"
    src_file = base_path / "business_models.json"
    dst_file = base_path / "business_models_enriched.json"

    with open(src_file, "r", encoding="utf-8") as f:
        models = json.load(f)

    for bm in models:
        bm_id = bm["id"]
        success = MAPPINGS.get(bm_id)

        if success is None:
            print(f"⚠ Warning: No mapping found for {bm_id}, defaulting to 0.70")
            success = 0.70

        bm["success_score"] = success
        bm["maturity_level"] = score_to_maturity(success)

    with open(dst_file, "w", encoding="utf-8") as f:
        json.dump(models, f, indent=2)

    print("✔ Enriched file written to:", dst_file)


if __name__ == "__main__":
    enrich_models()

