from textual.screen import ModalScreen
from textual.containers import Vertical, Center
from textual.widgets import Label, Button
from textual.app import ComposeResult

# Custom screen for game overrrr

class GameOverScreen(ModalScreen):
    def __init__(self, winner: str):
        super().__init__()
        if winner == "d":
            self.message = "DRAW! STALEMATE"
        else:
            self.message = f"CHECKMATE! {'WHITE' if winner == "w" else "BLACK"} WINS!"

    def compose(self) -> ComposeResult:
        with Center():
            with Vertical(id="dialog"):
                yield Label(self.message, id="msg")
                yield Button("New Game", variant="primary", id="new-game")
                yield Button("Exit", variant="error", id="exit")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "exit":
            self.app.exit()
        else:
            self.dismiss(True)


if __name__ == "__main__":
    GameOverScreen("w").run()