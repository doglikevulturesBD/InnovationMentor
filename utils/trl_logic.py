questions = [
    {"id": 1, "text": "Have the basic scientific principles been observed and reported?"},
    {"id": 2, "text": "Has a technology concept or application been formulated and validated in the lab?"},
    {"id": 3, "text": "Have key components or processes been validated experimentally?"},
    {"id": 4, "text": "Has a prototype been built and tested in a relevant (simulated) environment?"},
    {"id": 5, "text": "Has the prototype been demonstrated in an operational (real-world) environment?"},
    {"id": 6, "text": "Has the system been demonstrated under pre-commercial or pilot-scale conditions?"},
    {"id": 7, "text": "Is the system operating commercially in its intended environment?"}
]

def calculate_trl(answers):
    """
    Simple scoring logic:
    - Each 'Yes' increases TRL.
    - The last 'Yes' determines the TRL level.
    """
    score = 0
    for i, ans in enumerate(answers):
        if ans:
            score = i + 1
        else:
            break

    # Map 1–7 answers to 1–9 TRL scale roughly
    trl_map = [1, 2, 3, 5, 6, 8, 9]
    return trl_map[score-1] if score > 0 else 1

def trl_description(level):
    desc = {
        1: "Basic principles observed and reported.",
        2: "Technology concept and/or application formulated.",
        3: "Analytical and experimental proof of concept achieved.",
        4: "Component or breadboard validated in laboratory environment.",
        5: "Component or breadboard validated in relevant environment.",
        6: "System/subsystem model or prototype demonstrated in relevant environment.",
        7: "Prototype demonstrated in operational environment.",
        8: "System completed and qualified through test and demonstration.",
        9: "Actual system proven through successful operation."
    }
    return desc.get(level, "Unknown TRL")
