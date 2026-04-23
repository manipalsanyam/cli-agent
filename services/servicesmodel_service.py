from __future__ import annotations

import json
import urllib.request
import urllib.error

base_url: str = ""
active_model: str | None = None
_cache: list[str] = []


def init_model_service(url: str) -> None:
    global base_url
    base_url = url.rstrip("/")


def fetch_available_models(force: bool = False) -> list[str]:
    global _cache

    if _cache and not force:
        return _cache

    url = f"{base_url}/v1/models"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read().decode())
        _cache = [m["id"] for m in data.get("data", [])]

    except urllib.error.URLError as exc:
        raise ConnectionError(
            f"Cannot reach LM Studio at {base_url}: {exc.reason}"
        ) from exc
    except Exception as exc:
        raise RuntimeError(f"Unexpected error fetching models: {exc}") from exc

    return _cache


def set_active(model_name: str) -> None:
    global active_model
    active_model = model_name


def is_available(model_name: str) -> bool:
    return model_name in fetch_available_models()


def summary() -> str:
    status = active_model or "none selected"
    return f"Active model : {status}\nServer URL   : {base_url}"
