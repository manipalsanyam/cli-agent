from __future__ import annotations

import json
import urllib.request
import urllib.error


class ModelService:
   

    def __init__(self, base_url: str) -> None:
        self.base_url     = base_url.rstrip("/")
        self.active_model: str | None = None
        self._cache:       list[str]  = []

    

    def fetch_available_models(self, force: bool = False) -> list[str]:
        """
        Return model IDs from the server.
        Cached after first call; pass force=True to refresh.
        """
        if self._cache and not force:
            return self._cache

        url = f"{self.base_url}/v1/models"
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                data = json.loads(resp.read().decode())
            self._cache = [m["id"] for m in data.get("data", [])]
        except urllib.error.URLError as exc:
            raise ConnectionError(
                f"Cannot reach LM Studio at {self.base_url}: {exc.reason}"
            ) from exc
        except Exception as exc:
            raise RuntimeError(f"Unexpected error fetching models: {exc}") from exc

        return self._cache

    def set_active(self, model_name: str) -> None:
        self.active_model = model_name

    def is_available(self, model_name: str) -> bool:
        return model_name in self.fetch_available_models()

    def summary(self) -> str:
        status = self.active_model or "none selected"
        return f"Active model : {status}\nServer URL   : {self.base_url}"
