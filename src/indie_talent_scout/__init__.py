"""
indie-talent-scout: Autonomous Creative Talent & Subculture Scouting Engine for India
Powered by Exa AI Neural Search.
"""

__version__ = "0.1.0"
__author__ = "Sriram Kintada"

from .models import CreativeProspect, EvaluationScore, OutreachDraft, SearchConfig
from .core import IndieScoutEngine
from .evaluators import evaluate_candidate

__all__ = [
    "CreativeProspect",
    "EvaluationScore",
    "OutreachDraft",
    "SearchConfig",
    "IndieScoutEngine",
    "evaluate_candidate",
]
