from textual.app import App
from board import Board
from screens.board_ui import BoardScreen


# Version -> Alpha 1: Made a functionable chess game in terminal..
# Version -> Alpha 1.1: Added check for knight moveset and friendly fire :D
# Version -> Alpha 1.2: Added check for rook moveset and friendly fire ;-;
# Version -> Alpha 1.3: Added check for bishop, queen and king with friendly fire check *-* Next up is pawn... WISH ME LUCK T_T
# Version -> Alpha 1.4: Added pawn's moveset and ofc with friendly fire check :DDDDD. Easier than I thought.
# Version -> Alpha 1.5: Added move log and turn based movement
# Version -> Alpha 1.6: Added special cases like Pawn promotion, en passant and castling
# Version -> Alpha 1.7: Added check and pinning.
# Version -> Alpha 1.8: Added game over, changed UI and made it look better! Also added checkmating and check check iykyk
# Version -> Alpha Release: Made everything ready for alpha release

class ChessApp(App):
    CSS = """
Horizontal {
    height: 100%;
}

#sidebar {
    width: 30;
    background: $panel;
    dock: right;
    border-left: tall $accent;
    padding: 1;
}

#history-list {
    height: 1fr;
    border: solid $accent;
}

#sidebar-title {
    background: $primary;
    color: white;
    padding: 1;
    margin-bottom: 1;
    text-align: center;
}

ListItem {
    padding: 0 1;
}

#board-grid {
    layout: grid;
    grid-size: 8 8;
    grid-columns: 1fr;
    grid-rows: 1fr;
    width: 100;
    height: 50;
    align: center middle;
    border: round gold;
    padding: 0;
    margin: 1;
}

ChessPiece {
    width: 1fr;
    height: 1fr;
    content-align: center middle;
    border: none;
    min-width: 12;
    min-height: 6;
}

ChessPiece > Label {
    width: 100%;
    height: 100%;
    content-align: center middle;
}

ChessPiece:focus {
    text-style: none;
    border: round gold;
}

.light:hover, .light:focus {
    background: #ebecd0;
}

.dark:hover, .dark:focus {
    background: #779556;
}

.light {
    background: #ebecd0;
    color: #fdfdfd;
}

.dark {
    background: #779556;
    color: #fdfdfd;
}

.selected {
    text-style: italic;
}

.piece {
    text-style: bold;
}

#dialog {
    width: 50;
    height: 18;
    background: $panel;
    border: thick gold;
    padding: 1 2;
    content-align: center middle;
    margin-top: 10;
}
"""
    
    def on_mount(self) -> None:
        self.board = Board()
        self.install_screen(BoardScreen(self.board), name="game")
        self.push_screen("game")


if __name__ == "__main__":
    ChessApp().run()