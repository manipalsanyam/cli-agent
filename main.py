import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from services.ui_service import format_text, print_header as print_header_fn
from services.servicesmodel_service import fetch_available_models, set_active_model
from services.chat_service import get_chat_response

load_dotenv()
URL = os.getenv("LM_STUDIO_URL", "http://127.0.0.1:1234")
HISTORY_PATH = Path(__file__).resolve().parent / "chat_history.json"


class UIService:
    def format(self, text: str, color_key: str = "E") -> str:
        return format_text(text, color_key)

    def print_header(self) -> None:
        print_header_fn()


class ModelService:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.active_model = None

    def fetch_available_models(self):
        return fetch_available_models(self.base_url)

    def set_active(self, model_name: str):
        self.active_model = model_name


class ChatService:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.history = []
        self.message_count = 0

    def send_message(self, model: str, content: str) -> str:
        agent = {"history": self.history}
        response = get_chat_response(agent, content)
        self.message_count += 1
        return response

    def get_session_info(self, active_model: str) -> str:
        return (
            f"Model: {active_model}\n"
            f"Total messages: {len(self.history)}\n"
            f"Assistant replies: {self.message_count}"
        )


def ensure_service_path():
    project_root = Path(__file__).resolve().parent
    service_root = project_root / "Services"
    if service_root.exists() and str(service_root) not in sys.path:
        sys.path.insert(0, str(service_root))


def normalize_command(raw_input: str) -> str:
    return raw_input.strip().lower().lstrip("/")


def print_help(ui: UIService):
    print(ui.format("Commands:", "BD"))
    print(ui.format(" /help", "G") + " - Show this help message")
    print(ui.format(" /models", "G") + " - List available models")
    print(ui.format(" /switch <model>", "G") + " - Change the active model")
    print(ui.format(" /reset", "G") + " - Clear the conversation history")
    print(ui.format(" /history", "G") + " - Show the conversation history")
    print(ui.format(" /save [path]", "G") + " - Save session history to a JSON file")
    print(ui.format(" /load [path]", "G") + " - Load session history from a JSON file")
    print(ui.format(" /info", "G") + " - Show session stats")
    print(ui.format(" /quit", "G") + " - Exit the agent")


def print_models(models: ModelService, ui: UIService):
    available = models.fetch_available_models()
    if not available:
        print(ui.format("No models found.", "R"))
        return

    print(ui.format("Available models:", "BD"))
    for idx, model in enumerate(available, start=1):
        marker = "*" if model == models.active_model else " "
        print(f" {marker} {idx}. {model}")


def show_history(chat: ChatService, ui: UIService, limit: int = 10):
    if not chat.history:
        print(ui.format("No conversation history yet.", "Y"))
        return

    print(ui.format("Conversation history:", "BD"))
    recent = chat.history[-limit:]
    for entry in recent:
        role = "You" if entry["role"] == "user" else "Agent"
        color = "B" if entry["role"] == "user" else "C"
        print(f"{ui.format(role + ':', color)} {entry['content']}")


def reset_conversation(chat: ChatService, ui: UIService):
    chat.history.clear()
    chat.message_count = 0
    print(ui.format("Conversation history cleared.", "G"))


def save_history(chat: ChatService, ui: UIService, path: str | None = None):
    if not path:
        path = str(HISTORY_PATH)

    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(chat.history, fh, indent=2, ensure_ascii=False)
        print(ui.format(f"Saved history to {path}", "G"))
    except Exception as exc:
        print(ui.format(f"Unable to save history: {exc}", "R"))


def load_history(chat: ChatService, ui: UIService, path: str | None = None):
    if not path:
        path = str(HISTORY_PATH)

    try:
        with open(path, "r", encoding="utf-8") as fh:
            loaded = json.load(fh)
        if isinstance(loaded, list):
            chat.history = loaded
            chat.message_count = sum(1 for item in loaded if item.get("role") == "assistant")
            print(ui.format(f"Loaded history from {path}", "G"))
        else:
            raise ValueError("Invalid history format")
    except FileNotFoundError:
        print(ui.format(f"History file not found: {path}", "Y"))
    except Exception as exc:
        print(ui.format(f"Unable to load history: {exc}", "R"))


def switch_model(models: ModelService, ui: UIService, model_name: str):
    available = models.fetch_available_models()
    if model_name not in available:
        print(ui.format(f"Model '{model_name}' is not available.", "R"))
        return

    models.set_active(model_name)
    print(ui.format(f"Switched to model: {models.active_model}", "G"))


def parse_and_execute_command(raw: str, ui: UIService, models: ModelService, chat: ChatService) -> bool:
    command, *rest = raw.strip().split(maxsplit=1)
    command = normalize_command(command)
    arg = rest[0].strip() if rest else None

    if command in {"help", "h", "?"}:
        print_help(ui)
        return True
    if command == "models":
        print_models(models, ui)
        return True
    if command == "switch" and arg:
        switch_model(models, ui, arg)
        return True
    if command == "reset":
        reset_conversation(chat, ui)
        return True
    if command == "history":
        show_history(chat, ui)
        return True
    if command == "save":
        save_history(chat, ui, arg)
        return True
    if command == "load":
        load_history(chat, ui, arg)
        return True
    if command == "info":
        print(ui.format(chat.get_session_info(models.active_model), "C"))
        return True
    if command in {"quit", "exit"}:
        print(ui.format("Goodbye!", "G"))
        sys.exit(0)

    return False


def main():
    ensure_service_path()
    ui = UIService()
    models = ModelService(URL)
    chat = ChatService(URL)

    ui.print_header()
    print(ui.format("Type /help to see available commands.", "Y"))

    available = models.fetch_available_models()
    if not available:
        print(ui.format("❌ No models found or server offline", "R"))
        sys.exit(1)

    models.set_active(available[0])
    print(ui.format(f"Using: {models.active_model}", "G"))

    while True:
        raw_input = input(f"{ui.format('You:', 'B')} ").strip()
        if not raw_input:
            continue

        if raw_input.startswith("/") or normalize_command(raw_input) in {
            "help", "h", "?", "models", "switch", "reset", "history", "save", "load", "info", "quit", "exit"
        }:
            if parse_and_execute_command(raw_input, ui, models, chat):
                continue

        print(ui.format(" Thinking...", "Y"), end="", flush=True)
        response = chat.send_message(models.active_model, raw_input)
        print(f"\r{' '*50}\r{ui.format('Agent:', 'C')} {response}\n")


if __name__ == "__main__":
    main()
