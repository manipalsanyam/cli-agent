def send_chat(agent, prompt):
    """prompt = f"""
You are a strict classifier.

Choose ONLY one label from:
refund, late_delivery, wrong_item, complaint, general

Rules:
- Return only the label
- No explanation
- No sentence

Query: {user_input}
"""
    if hasattr(agent, "send_chat") and callable(agent.send_chat):
        return agent.send_chat(prompt)

    raise AttributeError("Agent must implement a callable send_chat(prompt) method")
