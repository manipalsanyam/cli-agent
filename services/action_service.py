from __future__ import annotations

import sys
from pathlib import Path


_DEFAULT_HISTORY_PATH = Path(__file__).resolve().parent.parent / "chat_history.json"


def handle_action(state: dict, raw: str) -> bool:
    parts   = raw.strip().split(maxsplit=1)
    command = _normalise(parts[0])
    arg     = parts[1].strip() if len(parts) > 1 else None

    dispatch = {
        "help":    lambda: _help(state),
        "h":       lambda: _help(state),
        "?":       lambda: _help(state),
        "models":  lambda: _models(state),
        "switch":  lambda: _switch(state, arg),
        "reset":   lambda: _reset(state),
        "history": lambda: _history(state),
        "save":    lambda: _save(state, arg),
        "load":    lambda: _load(state, arg),
        "info":    lambda: _info(state),
        "quit":    lambda: _quit(state),
        "exit":    lambda: _quit(state),
    }

    handler = dispatch.get(command)
    if handler is None:
        return False

    handler()
    return True


def _help(state: dict) -> None:
    state["ui"].print_help()


def _models(state: dict) -> None:
    try:
        available = state["models"].fetch_available_models(force=True)
    except ConnectionError as exc:
        state["ui"].error(str(exc))
        return

    if not available:
        state["ui"].warn("No models found on the server.")
        return

    print(state["ui"].format("Available models:", "BD"))
    for idx, name in enumerate(available, start=1):
        marker = "*" if name == state["models"].active_model else " "
        print(f"  {marker} {idx}. {name}")
    print()


def _switch(state: dict, model_name: str | None) -> None:
    if not model_name:
        state["ui"].warn("Usage: /switch <model-name>")
        return

    try:
        available = state["models"].fetch_available_models()
    except ConnectionError as exc:
        state["ui"].error(str(exc))
        return

    if model_name not in available:
        state["ui"].error(
            f"Model '{model_name}' not available. Run /models to see options."
        )
        return

    state["models"].set_active(model_name)
    state["ui"].info(f"Switched to: {model_name}")


def _reset(state: dict) -> None:
    state["chat"].reset()
    state["ui"].info("Conversation history cleared.")


def _history(state: dict) -> None:
    messages = state["chat"].recent(10)

    if not messages:
        state["ui"].warn("No conversation history yet.")
        return

    print(state["ui"].format("Recent conversation:", "BD"))
    for msg in messages:
        role  = "You" if msg["role"] == "user" else "Agent"
        color = "B"   if msg["role"] == "user" else "C"
        print(f"{state['ui'].format(role + ':', color)} {msg['content']}")
    print()


def _save(state: dict, path: str | None) -> None:
    target = Path(path) if path else state.get("history_path", _DEFAULT_HISTORY_PATH)

    try:
        state["chat"].save(target)
        state["ui"].info(f"History saved → {target}")
    except Exception as exc:
        state["ui"].error(f"Could not save: {exc}")


def _load(state: dict, path: str | None) -> None:
    target = Path(path) if path else state.get("history_path", _DEFAULT_HISTORY_PATH)

    try:
        state["chat"].load(target)
        state["ui"].info(f"History loaded ← {target}")
    except FileNotFoundError:
        state["ui"].warn(f"File not found: {target}")
    except ValueError as exc:
        state["ui"].error(f"Bad history format: {exc}")
    except Exception as exc:
        state["ui"].error(f"Could not load: {exc}")


def _info(state: dict) -> None:
    info = state["chat"].session_info(state["models"].active_model or "none")
    print(state["ui"].format(info, "C"))


def _quit(state: dict) -> None:
    state["ui"].exit("Goodbye!")


def _normalise(token: str) -> str:
    return token.strip().lower().lstrip("/")
How to use it (important)

Instead of creating a class instance, you now pass a state dictionary:

state = {
    "ui": ui_service,
    "models": model_service,
    "chat": chat_service,
    "history_path": None  # optional
}

handled = handle_action(state, user_input)
