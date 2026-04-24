from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum


class Intent(str, Enum):
    GREETING   = "greeting"
    FAREWELL   = "farewell"
    HELP       = "help"
    QUESTION   = "question"
    COMMAND    = "command"
    SMALL_TALK = "small_talk"
    UNKNOWN    = "unknown"


@dataclass
class IntentResult:
    intent:     Intent
    confidence: float   # 0.0 – 1.0
    raw_input:  str


_PATTERNS: list[tuple[re.Pattern[str], Intent, float]] = [
    (re.compile(r"\b(hi|hello|hey|good\s?(morning|evening|afternoon))\b", re.I),
     Intent.GREETING,   0.95),

    (re.compile(r"\b(bye|goodbye|see\s?you|farewell|quit|exit)\b", re.I),
     Intent.FAREWELL,   0.95),

    (re.compile(r"\b(help|how\s?to|explain|what\s?is|what\s?are)\b", re.I),
     Intent.HELP,       0.80),

    (re.compile(r"\?"),
     Intent.QUESTION,   0.70),

    (re.compile(r"^/"),
     Intent.COMMAND,    1.00),

    (re.compile(r"\b(thanks|thank\s?you|cheers|great|cool|nice)\b", re.I),
     Intent.SMALL_TALK, 0.75),
]


def classify_intent(text: str) -> IntentResult:
    text = text.strip()
    for pattern, intent, confidence in _PATTERNS:
        if pattern.search(text):
            return IntentResult(
                intent=intent,
                confidence=confidence,
                raw_input=text,
            )
    return IntentResult(intent=Intent.UNKNOWN, confidence=0.5, raw_input=text)


def is_command(text: str) -> bool:
    return text.strip().startswith("/")
