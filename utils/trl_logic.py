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
    1: "Basic principles observed and reported.",
    2: "Technology concept formulated.",
    3: "Analytical and experimental proof-of-concept achieved (lab).",
    4: "Components validated in laboratory environment.",
    5: "Subsystem validated in relevant environment.",
    6: "Prototype demonstrated in relevant (simulated) environment.",
    7: "Prototype demonstrated in operational environment (pilot).",
    8: "System completed and qualified through demonstration.",
    9: "System proven in successful commercial operation."
}

def calculate_trl(answers):
    """Stops at first 'No'; TRL = number of consecutive 'Yes'."""
    trl = 0
    for ans in answers:
        if ans:
            trl += 1
        else:
            break
    return min(trl, 9)

def trl_description(level):
    return trl_descriptions.get(level, "Unknown TRL")

