from __future__ import annotations

import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any


_DEFAULT_SYSTEM = (
    "You are a helpful, concise AI assistant running locally via LM Studio. "
    "Answer clearly and avoid unnecessary filler."
)

Message = dict[str, str]  # {"role": "user"|"assistant"|"system", "content": str}


class ChatService:
    """
    Owns conversation state and communicates with the LM Studio backend.

    Each instance keeps its own history so multiple sessions can run
    independently without sharing state.
    """

    def __init__(
        self,
        base_url:      str,
        system_prompt: str = _DEFAULT_SYSTEM,
    ) -> None:
        self.base_url      = base_url.rstrip("/")
        self.system_prompt = system_prompt
        self.history:       list[Message] = []
        self.message_count: int = 0

  

    def send_message(self, model: str, content: str) -> str:
        """
        Append user *content*, call the model, store and return the reply.
        Raises ConnectionError on network failure.
        """
        self.history.append({"role": "user", "content": content})

        messages: list[Message] = (
            [{"role": "system", "content": self.system_prompt}]
            + self.history
        )

        payload = json.dumps({
            "model":       model,
            "messages":    messages,
            "temperature": 0.7,
            "max_tokens":  -1,
            "stream":      False,
        }).encode()

        req = urllib.request.Request(
            url=f"{self.base_url}/v1/chat/completions",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data: dict[str, Any] = json.loads(resp.read().decode())
        except urllib.error.URLError as exc:
            # Remove the user message we just appended so history stays clean
            self.history.pop()
            raise ConnectionError(f"Request to LM Studio failed: {exc.reason}") from exc

        reply: str = data["choices"][0]["message"]["content"].strip()
        self.history.append({"role": "assistant", "content": reply})
        self.message_count += 1
        return reply


    def reset(self) -> None:
        self.history.clear()
        self.message_count = 0

    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as fh:
            json.dump(self.history, fh, indent=2, ensure_ascii=False)

    def load(self, path: str | Path) -> None:
        path = Path(path)
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, list):
            raise ValueError("History file must contain a JSON array.")
        self.history = data
        self.message_count = sum(1 for m in data if m.get("role") == "assistant")

    def recent(self, n: int = 10) -> list[Message]:
        return self.history[-n:]


    def session_info(self, active_model: str) -> str:
        return (
            f"Model            : {active_model}\n"
            f"Total messages   : {len(self.history)}\n"
            f"Assistant replies: {self.message_count}"
        )
