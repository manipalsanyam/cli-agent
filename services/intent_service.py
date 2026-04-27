from __future__ import annotations

import re
from typing import TypedDict


GREETING        = "greeting"
FAREWELL        = "farewell"
HELP            = "help"

ORDER_STATUS    = "order_status"
REFUND_REQUEST  = "refund_request"
CANCEL_ORDER    = "cancel_order"
COMPLAINT       = "complaint"
ESCALATION      = "escalation"

SMALL_TALK      = "small_talk"
COMMAND         = "command"
UNKNOWN         = "unknown"


class IntentResult(TypedDict):
    intent: str
    confidence: float
    raw_input: str



PATTERNS: list[tuple[re.Pattern[str], str, float]] = [

    
    (re.compile(r"^/"), COMMAND, 1.00),


    (re.compile(r"\b(hi|hello|hey)\b", re.I), GREETING, 0.95),
    (re.compile(r"\b(bye|goodbye|see you)\b", re.I), FAREWELL, 0.95),

    
    (re.compile(r"\b(order status|track order|where is my order|delivery status)\b", re.I),
     ORDER_STATUS, 0.95),

   
    (re.compile(r"\b(refund|money back|return my money)\b", re.I),
     REFUND_REQUEST, 0.95),

   
    (re.compile(r"\b(cancel order|cancel my order)\b", re.I),
     CANCEL_ORDER, 0.95),

    
    (re.compile(r"\b(bad|worst|not working|issue|problem|late|delay|damaged)\b", re.I),
     COMPLAINT, 0.80),

   
    (re.compile(r"\b(manager|human|support agent|talk to someone|complaint escalate)\b", re.I),
     ESCALATION, 0.90),

  
    (re.compile(r"\b(help|how to|what can you do)\b", re.I),
     HELP, 0.80),

    
    (re.compile(r"\b(thanks|thank you|great|nice)\b", re.I),
     SMALL_TALK, 0.70),
]



def classify(text: str) -> IntentResult:
    text = text.strip()

    for pattern, intent, confidence in PATTERNS:
        if pattern.search(text):
            return {
                "intent": intent,
                "confidence": confidence,
                "raw_input": text,
            }

    return {
        "intent": UNKNOWN,
        "confidence": 0.5,
        "raw_input": text,
    }


def is_command(text: str) -> bool:
    return text.strip().startswith("/")
