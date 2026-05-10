from textual.app import App
from board import Board
from screens.board_ui import BoardScreen


# Version -> Alpha 1: Making a functionable chess game in terminal..

class ChessApp(App):
    CSS_PATH = "style.tcss"
    
    def on_mount(self) -> None:
        self.board = Board()
        self.install_screen(BoardScreen(self.board), name="game")
        self.push_screen("game")


if __name__ == "__main__":
    ChessApp().run()