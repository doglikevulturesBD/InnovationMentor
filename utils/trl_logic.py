# utils/trl_logic.py

# 9 clear, ascending TRL checkpoints
questions = [
    {"id": 1, "text": "Have basic scientific principles been observed and reported? (TRL1)"},
    {"id": 2, "text": "Has the technology concept/application been formulated? (TRL2)"},
    {"id": 3, "text": "Do you have analytical & experimental proof-of-concept in the lab? (TRL3)"},
    {"id": 4, "text": "Have key components been validated in a laboratory environment? (TRL4)"},
    {"id": 5, "text": "Have integrated components/subsystems been validated in a relevant environment? (TRL5)"},
    {"id": 6, "text": "Has a prototype system been demonstrated in a relevant (simulated) environment? (TRL6)"},
    {"id": 7, "text": "Has a prototype/pilot been demonstrated in an operational environment? (TRL7)"},
    {"id": 8, "text": "Is the full system completed and qualified through test & demonstration? (TRL8)"},
    {"id": 9, "text": "Is the actual system proven in successful commercial operation? (TRL9)"},
]

# Optional: allow TRL 0 when even TRL1 is 'No'
ALLOW_TRL_ZERO = True

trl_descriptions = {
    0: "Pre-TRL: basic principles not yet observed/reported.",
    1: "Basic principles observed and reported.",
    2: "Technology concept/application formulated.",
    3: "Analytical & experimental proof-of-concept achieved (lab).",
    4: "Component/breadboard validated in laboratory environment.",
    5: "Integrated components/subsystem validated in relevant environment.",
    6: "System/subsystem prototype demonstrated in relevant environment.",
    7: "Prototype/pilot demonstrated in operational environment.",
    8: "System completed & qualified through test & demonstration.",
    9: "Actual system proven in commercial operation.",
}

def calculate_trl(answers: list[bool]) -> int:
    """
    Returns TRL = number of consecutive 'True' from the start.
    Stops counting at first False.
      []                  -> 0 (or 1 if ALLOW_TRL_ZERO=False)
      [True]              -> 1
      [True, True]        -> 2
      [True, False, ...]  -> 1
      [False, ...]        -> 0 (or 1 if ALLOW_TRL_ZERO=False)
      [True x9]           -> 9
    """
    level = 0
    for ans in answers:
        if ans:
            level += 1
        else:
            break
    if level == 0 and not ALLOW_TRL_ZERO:
        return 1
    return max(0, min(9, level))

def trl_description(level: int) -> str:
    return trl_descriptions.get(level, "Unknown TRL")

def get_trl_level(answers):
    lvl = calculate_trl(answers)
    return {"level": lvl, "description": trl_description(lvl)}

