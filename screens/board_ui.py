from textual.app import ComposeResult
from textual.widgets import Button, Header, Footer, Static
from textual.containers import Grid, Center
from textual.screen import Screen

class BoardScreen(Screen):
    def __init__(self, board_logic):
        super().__init__()
        self.board_logic = board_logic
        self.selected_pos = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            with Grid(id="board-grid"):
                for m in range(7,-1, -1):
                    for n in range(8):
                        piece = self.board_logic.board_format[m][n]
                        label = " " if piece == "0" else piece
                        
                        pos_name = self.board_logic.to_chess_notation(m,n)
                        btn = Button(label, id=pos_name)

                        btn.add_class("light" if (m + n) % 2 != 0 else "dark")
                        yield btn
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

            self.board_logic.move(self.selected_pos, current_pos)
            self.update_board_ui()

            # Reset
            self.query_one(f"#{self.selected_pos}").remove_class("selected")
            self.selected_pos = None
            
    def update_board_ui(self) -> None:
        for m in range(8):
            for n in range(8):
                piece = self.board_logic.board_format[m][n]
                label = " " if piece == "0" else piece
                pos_name = self.board_logic.to_chess_notation(m, n)
                self.query_one(f"#{pos_name}", Button).label = label