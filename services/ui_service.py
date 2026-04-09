class UIService:
    COLORS = {
        'B': '\033[94m', 'C': '\033[96m', 'G': '\033[92m',
        'Y': '\033[93m', 'R': '\033[91m', 'BD': '\033[1m', 'E': '\033[0m'
    }

    @classmethod
    def format(cls, text, color_key):
        return f"{cls.COLORS.get(color_key, '')}{text}{cls.COLORS['E']}"

    def print_header(self):
        print(f"\n{self.format('='*55, 'B')}")
        print(f"🤖 {self.format('LM Studio CLI Agent', 'BD')}")
        print(f"{self.format('-'*55, 'B')}\n")