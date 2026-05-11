from rich.text import Text
from textual.widgets import Button

PIXEL_ART = {
    # Pawn:
    "wP": "   ▒   \n  ▒▒▒  \n ▄▒▒▒▄ ",
    "bP": "  ▄█▄  \n  ███  \n ▄███▄ ",

    # Rook:
    "wR": " ▒ ▒ ▒ \n ▒▒▒▒▒ \n ▒▒▒▒▒ \n ░░░░░ ",
    "bR": " █ █ █ \n █████ \n █████ \n ▀▀▀▀▀ ",

    # Knight:
    "wN": "   ▒▒  \n  ▒░▒▒ \n ░  ▒▒ \n  ░▒▒▒░",
    "bN": "  ▄██  \n ▄█▀██ \n ▀  ██ \n  ▄███▄",

    # Bishop:
    "wB": "   ▒   \n  ▒▒▒  \n  ▒▒▒  \n ░▒▒▒░ ",
    "bB": "   █   \n  ███  \n  ███  \n ▄███▄ ",

    # Queen:
    "wQ": " ▒ ▒ ▒ \n ░▒▒▒░ \n  ▒▒▒  \n ░▒▒▒░ ",
    "bQ": " █ █ █ \n ▀███▀ \n  ███  \n ▄███▄ ",

    # King:
    "wK": "   ▒   \n ░▒▒▒░ \n  ▒▒▒  \n ░▒▒▒░ ",
    "bK": "   █   \n ▄███▄ \n  ███  \n ▄███▄ ",

    # Empty space:
    "0": "       \n       \n       \n       "
}

class ChessPiece(Button):
    def __init__(self, piece_code: str, **kwargs):
        self.piece_code = piece_code
        super().__init__(label="", **kwargs)

    def render(self) -> Text:
        art = PIXEL_ART.get(self.piece_code, " ")

        return Text(art, style="bold")