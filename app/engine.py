"""Configurable, data-driven fraud rules engine (synthetic, generic design)."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
import operator

OPS: dict[str, Callable] = {
    "gt": operator.gt, "gte": operator.ge, "lt": operator.lt,
    "lte": operator.le, "eq": operator.eq, "ne": operator.ne,
    "in": lambda a, b: a in b,
}

@dataclass(frozen=True)
class Rule:
    id: str
    description: str
    field: str
    op: str
    value: object
    weight: int  # points added to the risk score when the rule fires

    def evaluate(self, event: dict) -> bool:
        if self.field not in event:
            return False
        return bool(OPS[self.op](event[self.field], self.value))

DEFAULT_RULES = [
    Rule("R1", "SIM swap within 24h of port-out request", "hours_since_sim_swap", "lt", 24, 40),
    Rule("R2", "New device on account < 7 days old", "account_age_days", "lt", 7, 20),
    Rule("R3", "High-value device purchase", "order_amount", "gt", 1000, 15),
    Rule("R4", "Login from new country", "new_country", "eq", True, 25),
    Rule("R5", "Multiple failed OTP attempts", "failed_otp", "gte", 3, 25),
]

def decide(score: int) -> str:
    if score >= 70: return "DECLINE"
    if score >= 40: return "STEP_UP_AUTH"
    return "APPROVE"

def score_event(event: dict, rules: list[Rule] = DEFAULT_RULES) -> dict:
    fired = [r for r in rules if r.evaluate(event)]
    score = min(100, sum(r.weight for r in fired))
    return {
        "score": score,
        "decision": decide(score),
        "fired_rules": [{"id": r.id, "description": r.description, "weight": r.weight} for r in fired],
    }
