from services.chat_service import get_chat_response

def classify_intent(agent, user_input):
    prompt = f"""
You are a customer support classifier.

Classify the query into ONLY one:
refund, late_delivery, wrong_item, complaint, general

Return ONLY the label.

Query: {user_input}
"""

    response = get_chat_response(agent, prompt)
    return response.strip().lower()
