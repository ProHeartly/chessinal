from textual.app import App
from board import Board
from screens.board_ui import BoardScreen


# Version -> Alpha 1: Made a functionable chess game in terminal..
# Version -> Alpha 1.1: Added check for knight moveset and friendly fire :D
# Version -> Alpha 1.2: Added cehck for rook moveset and friendly fire ;-;

class ChessApp(App):
    CSS_PATH = "style.tcss"
    
    def on_mount(self) -> None:
        self.board = Board()
        self.install_screen(BoardScreen(self.board), name="game")
        self.push_screen("game")


if __name__ == "__main__":
    ChessApp().run()