# utils/trl_logic.py

questions = [
    {"id": 1, "text": "Have basic scientific principles been observed and reported?"},
    {"id": 2, "text": "Has the technology concept or application been formulated?"},
    {"id": 3, "text": "Has analytical and experimental proof-of-concept been achieved in the lab?"},
    {"id": 4, "text": "Have key components or processes been validated in a laboratory environment?"},
    {"id": 5, "text": "Have integrated components or subsystems been validated in a relevant environment?"},
    {"id": 6, "text": "Has a prototype system been demonstrated in a relevant (simulated) environment?"},
    {"id": 7, "text": "Has the prototype or pilot system been demonstrated in an operational environment?"},
    {"id": 8, "text": "Has the system been completed and qualified through test and demonstration?"},
    {"id": 9, "text": "Has the actual system been proven through successful operation in its intended environment?"}
]

trl_descriptions = {
    1: "Basic principles observed and reported — fundamental research only.",
    2: "Technology concept and/or application formulated — still theoretical but potential use identified.",
    3: "Analytical and experimental proof-of-concept achieved — initial lab validation.",
    4: "Component or breadboard validated in laboratory environment — small-scale prototype exists.",
    5: "Component or breadboard validated in relevant environment — larger prototype tested under realistic conditions.",
    6: "System/subsystem prototype demonstrated in relevant environment — nearing pre-commercial readiness.",
    7: "System prototype demonstrated in operational environment — pilot or field test completed.",
    8: "System completed and qualified through test and demonstration — pre-production version validated.",
    9: "Actual system proven through successful operation — commercial deployment achieved."
}

def calculate_trl(answers):
    """
    Calculates TRL level based on sequential yes/no answers.
    Each 'yes' must be consistent (once 'no' appears, subsequent yeses are ignored).
    """
    score = 0
    for i, ans in enumerate(answers):
        if ans:
            score = i + 1
        else:
            break
    return score if score > 0 else 1

def trl_description(level: int) -> str:
    return trl_descriptions.get(level, "Unknown TRL")

def get_trl_level(answers):
    """Helper for integration with other modules later."""
    return {
        "level": calculate_trl(answers),
        "description": trl_description(calculate_trl(answers))
    }
