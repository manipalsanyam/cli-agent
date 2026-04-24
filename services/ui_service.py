import sys


COLOURS: dict[str, str] = {
    "R":  "\033[91m",   # Red
    "G":  "\033[92m",   # Green
    "Y":  "\033[93m",   # Yellow
    "B":  "\033[94m",   # Blue
    "C":  "\033[96m",   # Cyan
    "E":  "\033[0m",    # Reset
    "BD": "\033[1m",    # Bold
    "W":  "\033[97m",   # White
}
RESET = "\033[0m"


class UIService:
    """Responsible for all user-facing terminal rendering."""

    def format(self, text: str, color_key: str = "E") -> str:
        code = COLOURS.get(color_key, RESET)
        return f"{code}{text}{RESET}"

    def print_header(self) -> None:
        lines = [
            "╔══════════════════════════════════════════╗",
            "║          LM Studio Chat Agent           ║",
            "║      Local AI — Microservice Edition    ║",
            "╚══════════════════════════════════════════╝",
        ]
        print()
        for line in lines:
            print(self.format(line, "C"))
        print()

    def print_help(self) -> None:
        print(self.format("Available commands:", "BD"))
        commands = [
            ("/help",           "Show this help message"),
            ("/models",         "List available models"),
            ("/switch <model>", "Switch to a different model"),
            ("/reset",          "Clear conversation history"),
            ("/history",        "Print recent conversation"),
            ("/save [path]",    "Save history to JSON file"),
            ("/load [path]",    "Load history from JSON file"),
            ("/info",           "Show session statistics"),
            ("/quit",           "Exit the agent"),
        ]
        for cmd, desc in commands:
            print(f"  {self.format(cmd, 'G')}  —  {desc}")
        print()

    def thinking(self) -> None:
        print(self.format(" Thinking...", "Y"), end="", flush=True)

    def clear_line(self) -> None:
        print(f"\r{' ' * 60}\r", end="", flush=True)

    def print_agent_reply(self, text: str) -> None:
        print(f"{self.format('Agent:', 'C')} {text}\n")

    def print_user_prompt(self) -> str:
        return self.format("You: ", "B")

    def info(self, text: str) -> None:
        print(self.format(text, "G"))

    def warn(self, text: str) -> None:
        print(self.format(text, "Y"))

    def error(self, text: str) -> None:
        print(self.format(text, "R"))

    def exit(self, message: str = "Goodbye!", code: int = 0) -> None:
        self.info(message)
        sys.exit(code)
