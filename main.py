from textual.app import App
from board import Board
from screens.board_ui import BoardScreen


# Version -> Alpha 1: Made a functionable chess game in terminal..
# Version -> Alpha 1.1: Added check for knight moveset and friendly fire :D
# Version -> Alpha 1.2: Added check for rook moveset and friendly fire ;-;
# Version -> Alpha 1.3: Added check for bishop, queen and king with friendly fire check *-* Next up is pawn... WISH ME LUCK T_T

class ChessApp(App):
    CSS_PATH = "style.tcss"
    
    def on_mount(self) -> None:
        self.board = Board()
        self.install_screen(BoardScreen(self.board), name="game")
        self.push_screen("game")


if __name__ == "__main__":
    ChessApp().run()