

# This script will handle the board config and positions..

class Board:
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # uhhh, don't judge me for this
        self.w_pawn = "wP"
        self.w_rook = "wR"
        self.w_queen = "wQ"
        self.w_bishop = "wB"
        self.w_king = "wK"
        self.w_knight = "wN"

        self.b_pawn = "bP"
        self.b_rook = "bR"
        self.b_queen = "bQ"
        self.b_bishop = "bB"
        self.b_king = "bK"
        self.b_knight = "bN"
        self.alpha = {
            "a": 0,
            "b": 1,
            "c": 2,
            "d": 3,
            "e": 4,
            "f": 5,
            "g": 6,
            "h": 7
        } # Nice idea right????

        self.inv_alpha = {
            0: "a",
            1: "b",
            2: "c",
            3: "d",
            4: "e",
            5: "f",
            6: "g",
            7: "h"
        }

        self.board_format = [
            [self.w_rook, self.w_knight, self.w_bishop, self.w_queen, self.w_king, self.w_bishop, self.w_knight, self.w_rook],
            [self.w_pawn, self.w_pawn, self.w_pawn, self.w_pawn, self.w_pawn, self.w_pawn, self.w_pawn, self.w_pawn],
            ["0", "0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0", "0"],
            [self.b_pawn, self.b_pawn, self.b_pawn, self.b_pawn, self.b_pawn, self.b_pawn, self.b_pawn, self.b_pawn],
            [self.b_rook, self.b_knight, self.b_bishop, self.b_queen, self.b_king, self.b_bishop, self.b_knight, self.b_rook],
        ] # I typed this all with my handss
        
    def to_chess_notation(self, m: int, n: int):
        # (0, 0) -> "a1"
        return f"{self.inv_alpha[n]}{m+1}"
    
    def parse_pos(self, pos:str):
        # "a1" -> (0, 0)
        n = self.alpha[pos[0].lower()]
        m = int(pos[1]) - 1
        return m,n

    def what_in_pos(self, pos: str) -> str: 
        # This returns what piece is in that position. Usage: what_in_pos(board, "d1") -> w_qn
        m, n = self.parse_pos(pos)
        return self.board_format[m][n]
    
    def is_legal_knight_move(self, m1, n1, m2, n2):
        row_diff = abs(m1 - m2)
        col_diff = abs(n1 - n2)

        # A knight moves in L shape (2, 1) or (1, 2)
        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            start_piece = self.board_format[m1][n1]
            end_piece = self.board_format[m2][n2]

            if end_piece != "0":
                if start_piece[0] == end_piece[0]:
                    return False
            return True
        return False
    
    def move(self, pos1: str, pos2: str) -> bool:
        m1, n1 = self.parse_pos(pos1)
        m2, n2 = self.parse_pos(pos2)
        piece = self.board_format[m1][n1]

        if piece.endswith("N"):
            if not self.is_legal_knight_move(m1, n1, m2, n2):
                return False

        self.board_format[m2][n2] = self.what_in_pos(pos1)
        self.board_format[m1][n1] = "0"
        return True
        