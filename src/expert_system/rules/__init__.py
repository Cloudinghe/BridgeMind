"""
专家系统规则
Expert System Rules

桥牌专家规则定义和实现
"""

from .basic_rules import get_basic_rules, OpeningRules, ResponseRules, TacticRules, SafetyRules
from .extended_rules import get_extended_rules

__all__ = [
    "get_basic_rules",
    "get_extended_rules",
    "OpeningRules",
    "ResponseRules",
    "TacticRules",
    "SafetyRules",
]
