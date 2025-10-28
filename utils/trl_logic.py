# utils/trl_logic.py

from typing import List

# Toggle: if False, the minimum returned TRL will be 1
ALLOW_TRL_ZERO = True

# Ordered, linear checkpoints for TRL 1..9
questions = [
    {"id": 1, "text": "Have basic scientific principles been observed and reported? (TRL 1)"},
    {"id": 2, "text": "Has the technology concept/application been formulated? (TRL 2)"},
    {"id": 3, "text": "Is there analytical & experimental proof-of-concept in the lab? (TRL 3)"},
    {"id": 4, "text": "Have key components been validated in a laboratory environment? (TRL 4)"},
    {"id": 5, "text": "Have integrated components/subsystems been validated in a relevant environment? (TRL 5)"},
    {"id": 6, "text": "Has a prototype system been demonstrated in a relevant (simulated) environment? (TRL 6)"},
    {"id": 7, "text": "Has a prototype/pilot been demonstrated in an operational environment? (TRL 7)"},
    {"id": 8, "text": "Is the full system completed and qualified through test & demonstration? (TRL 8)"},
    {"id": 9, "text": "Is the actual system proven in successful commercial operation? (TRL 9)"},
]

trl_descriptions = {
    0: "Pre-TRL: basic scientific principles not yet observed/reported.",
    1: "Basic principles observed and reported.",
    2: "Technology concept/application formulated.",
    3: "Analytical & experimental proof-of-concept achieved (lab).",
    4: "Components/breadboard validated in laboratory environment.",
    5: "Integrated components/subsystems validated in relevant environment.",
    6: "System/subsystem prototype demonstrated in relevant environment.",
    7: "Prototype/pilot demonstrated in operational environment.",
    8: "System completed & qualified through test & demonstration.",
    9: "Actual system proven in successful commercial operation.",
}

def calculate_trl(answers: List[bool]) -> int:
    """
    TRL = number of consecutive 'True' from the start.
    Stops counting at the first False.
    Examples:
      []                     -> 0 (or 1 if ALLOW_TRL_ZERO=False)
      [True]                 -> 1
      [True, True, False]    -> 2
      [False, ...]           -> 0 (or 1 if ALLOW_TRL_ZERO=False)
      [True x 9]             -> 9
    """
    level = 0
    for a in answers:
        if a: level += 1
        else: break

    if level == 0 and not ALLOW_TRL_ZERO:
        return 1
    return max(0, min(level, 9))

def trl_description(level: int) -> str:
    return trl_descriptions.get(level, "Unknown TRL")

def next_trl_description(level: int) -> str:
    if level >= 9: return "You are at the highest TRL."
    nxt = level + 1
    return trl_descriptions.get(nxt, "")

