import requests

class ModelService:
    def __init__(self, base_url):
        self.api_url = f"{base_url}/v1/models"
        self.active_model = None

    def fetch_available_models(self):
        try:
            r = requests.get(self.api_url, timeout=5)
            return [m["id"] for m in r.json().get("data", [])] if r.status_code == 200 else []
        except:
            return []

    def set_active(self, model_name):
        self.active_model = model_name