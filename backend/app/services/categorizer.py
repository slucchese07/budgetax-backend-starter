from dataclasses import dataclass
from typing import Optional

@dataclass
class Rule:
    contains: str
    category_name: str
    deductible: bool
    ato_label: Optional[str] = None

DEFAULT_RULES = [
    Rule(contains="WOOLWORTHS", category_name="Groceries", deductible=False, ato_label=None),
    Rule(contains="BUNNINGS", category_name="Tools & Equipment", deductible=True, ato_label="Work-related expenses"),
    Rule(contains="UBER", category_name="Transport", deductible=True, ato_label="Travel expenses"),
]

def apply_rules(description: str) -> tuple[Optional[str], Optional[bool], Optional[str]]:
    d = description.upper()
    for r in DEFAULT_RULES:
        if r.contains in d:
            return r.category_name, r.deductible, r.ato_label
    return None, None, None
