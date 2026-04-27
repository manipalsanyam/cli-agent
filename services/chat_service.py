from __future__ import annotations

import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any, TypedDict


DEFAULT_SYSTEM = (
    "You are a helpful, concise AI assistant running locally via LM Studio. "
    "Answer clearly and avoid unnecessary filler."
)



Message = dict[str, str]

class ChatSession(TypedDict):
    base_url: str
    system_prompt: str
    history: list[Message]
    message_count: int



def create_session(base_url: str, system_prompt: str = DEFAULT_SYSTEM) -> ChatSession:
    return {
        "base_url": base_url.rstrip("/"),
        "system_prompt": system_prompt,
        "history": [],
        "message_count": 0,
    }



def send_message(session: ChatSession, model: str, content: str) -> str:
    session["history"].append({"role": "user", "content": content})

    messages = (
        [{"role": "system", "content": session["system_prompt"]}]
        + session["history"]
    )

    payload = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False,
    }).encode()

    req = urllib.request.Request(
        url=f"{session['base_url']}/v1/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data: dict[str, Any] = json.loads(resp.read().decode())
    except urllib.error.URLError as exc:
        session["history"].pop()
        raise ConnectionError(f"Request to LM Studio failed: {exc.reason}") from exc

    reply = data["choices"][0]["message"]["content"].strip()
    session["history"].append({"role": "assistant", "content": reply})
    session["message_count"] += 1

    return reply



def reset_session(session: ChatSession) -> None:
    session["history"].clear()
    session["message_count"] = 0



def save_session(session: ChatSession, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as fh:
        json.dump(session["history"], fh, indent=2, ensure_ascii=False)



def load_session(session: ChatSession, path: str | Path) -> None:
    path = Path(path)

    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    if not isinstance(data, list):
        raise ValueError("History file must contain a JSON array.")

    session["history"] = data
    session["message_count"] = sum(
        1 for m in data if m.get("role") == "assistant"
    )


def recent_messages(session: ChatSession, n: int = 10) -> list[Message]:
    return session["history"][-n:]



def session_info(session: ChatSession, active_model: str) -> str:
    return (
        f"Model            : {active_model}\n"
        f"Total messages   : {len(session['history'])}\n"
        f"Assistant replies: {session['message_count']}"
    )
