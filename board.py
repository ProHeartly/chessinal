

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

        self.turn = "w" # "w" for white and "b" for black-
        self.move_history = []
        self.en_passant_target = None
        self.moved_status = {
            "wK": False, "wR_a": False, "wR_h": False,
            "bK": False, "bR_a": False, "bR_h": False
        }
        
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
    
    def is_legal_knight_move(self, m1, n1, m2, n2) -> bool:
        row_diff = abs(m1 - m2)
        col_diff = abs(n1 - n2)

        # A knight moves in L shape (2, 1) or (1, 2)
        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            start_piece = self.board_format[m1][n1]
            end_piece = self.board_format[m2][n2]

            if end_piece != "0":
                if start_piece[0] == end_piece[0]: # Friendly fire check
                    return False
            return True
        return False
    
    def is_legal_rook_move(self, m1, n1, m2, n2) -> bool:
        if m1 != m2 and n1 != n2: # Must be same row or column
            return False
        
        row_step = 0 if m1 == m2 else (1 if m2 > m1 else -1)
        col_step = 0 if n1 == n2 else (1 if n2 > n1 else -1)

        curr_m, curr_n = m1 + row_step, n1 + col_step

        while (curr_m, curr_n) != (m2, n2):
            if self.board_format[curr_m][curr_n] != "0":
                return False
            curr_m += row_step
            curr_n += col_step

        target = self.board_format[m2][n2]
        if target != "0" and target[0] == self.board_format[m1][n1][0]: # friendly fire check
            return False
        return True
    
    def is_legal_bishop_move(self, m1, n1, m2, n2) -> bool:
        row_diff = abs(m1 - m2)
        col_diff = abs(n1 - n2)

        if row_diff != col_diff: # Perfect diagonal
            return False
        
        row_step = (1 if m2 > m1 else -1)
        col_step = (1 if n2 > n1 else -1)

        curr_m, curr_n = m1 + row_step, n1 + col_step
        while (curr_m, curr_n) != (m2, n2):
            if self.board_format[curr_m][curr_n] != "0":
                return False
            curr_m += row_step
            curr_n += col_step

        target = self.board_format[m2][n2]
        if target != "0" and target[0] == self.board_format[m1][n1][0]: # friendly fire check
            return False
        return True
    
    def is_legal_king_move(self, m1, n1, m2, n2) -> bool:
        row_diff = abs(m1 - m2)
        col_diff = abs(n1 - n2)

        if row_diff <= 1 and col_diff <= 1:
            target = self.board_format[m2][n2]
            if target != "0" and target[0] == self.board_format[m1][n1][0]: # Friendly fire check 0-0
                return False
            return True
        return False
    
    def is_legal_pawn_move(self, m1, n1, m2, n2) -> bool:
        piece = self.board_format[m1][n1]
        direction = 1 if piece.startswith("w") else -1
        start_row = 1 if piece.startswith("w") else 6

        target = self.board_format[m2][n2]

        if n1 == n2 and target == "0": # Single square move
            if m2 == m1 + direction:
                return True
            
            if m1 == start_row and m2 == m1 + 2 * direction: # The begining 2 square move
                if self.board_format[m1 + direction][n1] == "0":
                    return True

        # First part was easy but I gotta think a little for diagonal *thinking*  

        if abs(n1 - n2) == 1 and m2 == m1 + direction:
            if target != "0" and target[0] != piece[0]: # checks for piece + friendly fire :DDD
                return True
            
        return False
    
    def can_castle(self, side: str) -> bool:
        # side is "w_king", "w_queen", "b_king", "b_queen"
        color = side[0]
        row = 0 if color == "w" else 7

        if self.moved_status[f"{color}K"]:
            return False
        
        if "king" in side:
            rook_key = f"{color}R_h"
            path = [5, 6]
        else:
            rook_key = f"{color}R_a"
            path = [1, 2, 3]

        if self.moved_status[rook_key]:
            return False
        
        for col in path:
            if self.board_format[row][col] != "0":
                return False
            
        return True
    
    def move(self, pos1: str, pos2: str) -> bool:
        m1, n1 = self.parse_pos(pos1)
        m2, n2 = self.parse_pos(pos2)
        piece = self.board_format[m1][n1]
        direction = 1 if piece.startswith("w") else -1

        if not piece.startswith(self.turn):
            return False
        
        move_note = ""

        if piece.endswith("K") and abs(n1 - n2) == 2: # Castle logic
            side_str = "king" if n2 > n1 else "queen" # long castle or short castle
            castle_key = f"{piece[0]}_{side_str}"
            if not self.can_castle(castle_key):
                return False
            
            # Movement of rookiiieee
            row = m1
            if side_str == "king":
                self.board_format[row][5] = self.board_format[row][7]
                self.board_format[row][7] = "0"
                move_note = "O-O"

            else:
                self.board_format[row][3] = self.board_format[row][0]
                self.board_format[row][0] = "0"
                move_note = "O-O-O"
            
            # Movement of kING-kun
            self.board_format[m2][n2] = piece
            self.board_format[m1][n1] = "0"
            self.moved_status[f"{piece[0]}K"] = True

        else:
            legal = False
            if piece.endswith("N"):
                legal = self.is_legal_knight_move(m1, n1, m2, n2)
            elif piece.endswith("R"):
                legal = self.is_legal_rook_move(m1, n1, m2, n2)
            elif piece.endswith("B"):
                legal = self.is_legal_bishop_move(m1, n1, m2, n2)
            elif piece.endswith("Q"):
                legal = self.is_legal_rook_move(m1, n1, m2, n2) or self.is_legal_bishop_move(m1, n1, m2, n2)
            elif piece.endswith("K"):
                legal = self.is_legal_king_move(m1, n1, m2, n2)
            elif piece.endswith("P"):
                is_ep = abs(n1 - n2) == 1 and m2 == m1 + direction and (m2, n2) == self.en_passant_target
                if is_ep: # En passant checkkkk
                    self.board_format[m1][n2] = "0"
                    legal = True
                    move_note = f"{pos1}x{pos2} (En Passant)"
                else:
                    legal = self.is_legal_pawn_move(m1, n1, m2, n2)

            if not legal: return False
            
            # Execute Move
            self.board_format[m2][n2] = piece
            self.board_format[m1][n1] = "0"

            # Update Moved Status for future castling
            if piece.endswith("K"): self.moved_status[f"{piece[0]}K"] = True
            if piece.endswith("R"):
                suffix = "a" if n1 == 0 else "h"
                self.moved_status[f"{piece[0]}R_{suffix}"] = True

            # Promotion & En Passant state
            if piece.endswith("P"):
                if m2 in [0, 7]:
                    self.board_format[m2][n2] = piece[0] + "Q"
                    move_note = f"{pos2}=Q"
                self.en_passant_target = (m1 + direction, n1) if abs(m1 - m2) == 2 else None
            else:
                self.en_passant_target = None

        if not move_note:
            move_note = f"{piece}:{pos1}->{pos2}"

        self.move_history.append(move_note)
        self.turn = "b" if self.turn == "w" else "w"
        return True
        