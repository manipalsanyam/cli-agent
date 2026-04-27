import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from dotenv import load_dotenv
load_dotenv()

from Services import (
    UIService,
    ChatService,
    IntentService,
    ActionService,
    ModelService,
)

URL = os.getenv("LM_STUDIO_URL") or "http://127.0.0.1:1234"


def initialize_services():
    """Initialize and return all services."""
    ui = UIService()
    models = ModelService(URL)
    chat = ChatService(URL)
    intent = IntentService()
    actions = ActionService(ui=ui, models=models, chat=chat)

    return ui, models, chat, intent, actions


def setup_model(ui, models):
    """Fetch and set active model."""
    try:
        available = models.fetch_available_models()
    except ConnectionError as exc:
        ui.error(f"❌ Unable to connect to LM Studio: {exc}")
        sys.exit(1)

    if not available:
        ui.error("❌ No models found. Please start LM Studio and load a model.")
        sys.exit(1)

    models.set_active(available[0])
    ui.info(f"Using model: {models.active_model}")
    print()


def chat_loop(ui, models, chat, intent, actions):
    """Main interaction loop."""
    while True:
        try:
            raw = input(ui.print_user_prompt()).strip()
        except (KeyboardInterrupt, EOFError):
            ui.exit("\nGoodbye!")

        if not raw:
            continue

      
        if intent.is_command(raw):
            try:
                actions.handle(raw)
            except Exception as exc:
                ui.error(f"Command error: {exc}")
            continue

        
        ui.thinking()
        try:
            reply = chat.send_message(models.active_model, raw)
        except ConnectionError as exc:
            ui.clear_line()
            ui.error(f"Connection error: {exc}")
            continue
        except Exception as exc:
            ui.clear_line()
            ui.error(f"Unexpected error: {exc}")
            continue

        ui.clear_line()
        ui.print_agent_reply(reply)


def main():
    ui, models, chat, intent, actions = initialize_services()

    ui.print_header()
    ui.warn("Type /help to see available commands.\n")

    setup_model(ui, models)
    chat_loop(ui, models, chat, intent, actions)


if __name__ == "__main__":
    main()
