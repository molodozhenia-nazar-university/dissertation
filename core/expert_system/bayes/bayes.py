import json
from typing import Dict, Any


def load_rule_base(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def apply_bayes_rule(rule_id: str, rule_base: Dict[str, Any]) -> str:

    rule = rule_base.get(rule_id)
    if rule is None:
        raise ValueError(f"Rule '{rule_id}' not found in rule_base.json")

    options = rule.get("options", {})
    if not options:
        raise ValueError(f"Rule '{rule_id}' has no options")

    best_target = None
    best_score = -1.0

    for option_name, data in options.items():
        p_h_given_e = float(data.get("p_h_given_e", 0.0))
        weight = float(data.get("weight", 1.0))

        score = p_h_given_e * weight

        print(
            f"[{rule_id}] option={option_name}, p_h_given_e={p_h_given_e}, "
            f"weight={weight}, score={score}"
        )

        if score > best_score:
            best_score = score
            best_target = data.get("target")

    if best_target is None:
        raise ValueError(f"Rule '{rule_id}' has no valid target")

    return best_target
