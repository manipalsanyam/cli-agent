import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from dotenv import load_dotenv
load_dotenv()

from Services import (
    UIService,
    ChatService,
    IntentService,
    ActionService,
    ModelService,
)

URL = os.getenv("LM_STUDIO_URL", "http://127.0.0.1:1234")


def main() -> None:
    ui      = UIService()
    models  = ModelService(URL)
    chat    = ChatService(URL)
    intent  = IntentService()
    actions = ActionService(ui=ui, models=models, chat=chat)

    ui.print_header()
    ui.warn("Type /help to see available commands.")

    try:
        available = models.fetch_available_models()
    except ConnectionError as exc:
        ui.error(f"❌  {exc}")
        sys.exit(1)

    if not available:
        ui.error("❌  No models found. Is LM Studio running?")
        sys.exit(1)

    models.set_active(available[0])
    ui.info(f"Using model: {models.active_model}")
    print()

    while True:
        try:
            raw = input(ui.print_user_prompt()).strip()
        except (KeyboardInterrupt, EOFError):
            ui.exit("\nGoodbye!")

        if not raw:
            continue

        if intent.is_command(raw):
            actions.handle(raw)
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


if __name__ == "__main__":
    main()
