from textual.app import ComposeResult
from textual.widgets import Button, Header, Footer, Static, Label, ListView, ListItem
from textual.containers import Grid, Center, Horizontal, Vertical
from textual.screen import Screen

from custom.button import ChessPiece
from screens.game_over import GameOverScreen

class BoardScreen(Screen):
    def __init__(self, board_logic):
        super().__init__()
        self.board_logic = board_logic
        self.selected_pos = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Center():
                with Grid(id="board-grid"):
                    for m in range(7,-1, -1):
                        for n in range(8):
                            piece = self.board_logic.board_format[m][n]

                            pos_name = self.board_logic.to_chess_notation(m,n)
                            btn = ChessPiece(piece, id=pos_name)

                            btn.add_class("light" if (m + n) % 2 != 0 else "dark")
                            yield btn
                with Vertical(id="sidebar"):
                    yield Label("Move History", id="sidebar-title")
                    yield Label(f"Current Turn: White", id="turn-display")
                    yield ListView(id="history-list")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        current_pos = event.button.id

        if self.selected_pos is None:
            if self.board_logic.what_in_pos(current_pos) != "0":
                self.selected_pos = current_pos
                event.button.add_class("selected")

        else:
            if self.selected_pos == current_pos:
                event.button.remove_class("selected")
                self.selected_pos = None
                return

            sucess = self.board_logic.move(self.selected_pos, current_pos)

            if sucess:
                self.update_board_ui()
                winner = self.board_logic.check_game_over()

                if winner:
                    self.app.push_screen(GameOverScreen(winner), self.handle_restart)
            else:
                self.app.notify("Invalid move!!", severity="error")

            # Reset
            self.query_one(f"#{self.selected_pos}").remove_class("selected")
            self.selected_pos = None
            
    def update_board_ui(self) -> None:
        for m in range(8):
            for n in range(8):
                piece = self.board_logic.board_format[m][n]
                pos_name = self.board_logic.to_chess_notation(m, n)
                target_btn = self.query_one(f"#{pos_name}", ChessPiece)
                target_btn.piece_code = piece
                target_btn.refresh()

        turn_label = self.query_one("#turn-display", Label)
        turn_text = "WHITE" if self.board_logic.turn == "w" else "BLACK"
        turn_label.update(f"Current Turn: {turn_text}")

        if self.board_logic.move_history:
            last_move = self.board_logic.move_history[-1]
            self.query_one("#history-list", ListView).append(ListItem(Label(last_move)))

    def handle_restart(self, should_restart: bool):
        if should_restart:
            self.board_logic.reset_board()
            self.update_board_ui()
            self.query_one("#history-list").clear()