from services.chat_service import get_chat_response

def classify_intent(agent, user_input):
 prompt = f"""
You are a strict customer support classifier.

Classify the query into EXACTLY one of these:
refund, late_delivery, wrong_item, complaint, general

Rules:
- Return ONLY the label
- No explanation
- No sentence
- No extra words

Examples:
Query: my order is late → late_delivery
Query: I want refund → refund

Now classify:

Query: {user_input}
"""

    response = get_chat_response(agent, prompt)
    return response.strip().lower().split()[0]
