def send_chat(agent, prompt):
    """Send a chat prompt through the provided agent.

    The agent is expected to expose a `send_chat(prompt)` method.
    """
    if hasattr(agent, "send_chat") and callable(agent.send_chat):
        return agent.send_chat(prompt)

    raise AttributeError("Agent must implement a callable send_chat(prompt) method")
