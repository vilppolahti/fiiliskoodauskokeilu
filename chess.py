# Simple Chess Game
# Why text-based? Simplest implementation that still captures chess rules without graphical complexity
# Why class-based? Encapsulates game state and rules in a clean, maintainable structure

class Chess:
    # Why 8x8 board? Standard chess board dimensions
    def __init__(self):
        self.board = self.initialize_board()
        self.current_player = 'white'  # Why start with white? Standard chess convention
        self.game_over = False
        self.checkmate = False

    # Why initialize with standard setup? Familiar starting position for chess players
    def initialize_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]
        
        # Why place pawns on second row? Standard chess starting position
        for i in range(8):
            board[1][i] = ('pawn', 'black')
            board[6][i] = ('pawn', 'white')
        
        # Why place pieces in order: rook, knight, bishop, queen, king, bishop, knight, rook? Standard arrangement
        pieces_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for i, piece in enumerate(pieces_order):
            board[0][i] = (piece, 'black')
            board[7][i] = (piece, 'white')
        
        return board

    # Why print board? Provides visual feedback in text-based interface
    def print_board(self):
        print('  a b c d e f g h')
        print(' +-----------------+')
        for y in range(8):
            row_str = f'{8-y}|'
            for x in range(8):
                piece = self.board[y][x]
                if piece:
                    symbol = self.get_piece_symbol(piece)
                    row_str += f'{symbol}|'
                else:
                    row_str += ' |'
            print(row_str)
            print(' +-----------------+')

    # Why use standard algebraic notation? Universally recognized chess symbols
    def get_piece_symbol(self, piece):
        piece_type, color = piece
        symbols = {
            'pawn': 'P', 'rook': 'R', 'knight': 'N', 
            'bishop': 'B', 'queen': 'Q', 'king': 'K'
        }
        symbol = symbols.get(piece_type, '?')
        return symbol.lower() if color == 'black' else symbol

    # Why validate move? Ensures only legal chess moves are executed
    def is_valid_move(self, start, end):
        start_piece = self.board[start[1]][start[0]]
        if not start_piece:
            return False
        
        piece_type, color = start_piece
        if color != self.current_player:
            return False  # Why check color? Players can only move their own pieces

        end_piece = self.board[end[1]][end[0]]
        if end_piece and end_piece[1] == color:
            return False  # Why prevent capturing own pieces? Standard chess rule

        # Why check piece-specific movement rules? Each piece moves differently
        dx = end[0] - start[0]
        dy = end[1] - start[1]

        if piece_type == 'pawn':
            direction = -1 if color == 'white' else 1
            # Why allow forward move? Pawns move forward
            if dx == 0 and dy == direction and not end_piece:
                return True
            # Why allow double forward from start? Pawns can move two squares from starting position
            if dx == 0 and dy == 2 * direction and start[1] == (1 if color == 'black' else 6) and not end_piece and not self.board[start[1] + direction][start[0]]:
                return True
            # Why allow diagonal capture? Pawns capture diagonally
            if abs(dx) == 1 and dy == direction and end_piece:
                return True
            return False

        elif piece_type == 'rook':
            # Why check straight line? Rooks move horizontally or vertically
            if dx == 0 or dy == 0:
                return self.is_path_clear(start, end)
            return False

        elif piece_type == 'knight':
            # Why check L-shape? Knights move in L-pattern (2 squares one direction, 1 square perpendicular)
            return (abs(dx) == 2 and abs(dy) == 1) or (abs(dx) == 1 and abs(dy) == 2)

        elif piece_type == 'bishop':
            # Why check diagonal? Bishops move diagonally
            if abs(dx) == abs(dy):
                return self.is_path_clear(start, end)
            return False

        elif piece_type == 'queen':
            # Why check straight or diagonal? Queens combine rook and bishop movement
            if (dx == 0 or dy == 0) or (abs(dx) == abs(dy)):
                return self.is_path_clear(start, end)
            return False

        elif piece_type == 'king':
            # Why check one square? Kings move one square in any direction
            return abs(dx) <= 1 and abs(dy) <= 1

        return False

    # Why check path? Ensures pieces dont jump over other pieces (except knights)
    def is_path_clear(self, start, end):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        steps = max(abs(dx), abs(dy))
        
        for i in range(1, steps):
            x = start[0] + (dx * i) // steps
            y = start[1] + (dy * i) // steps
            if self.board[y][x]:
                return False
        return True

    # Why check for check? Core chess rule that determines valid moves
    def is_in_check(self, color):
        king_pos = None
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece and piece[0] == 'king' and piece[1] == color:
                    king_pos = (x, y)
                    break
            if king_pos:
                break

        if not king_pos:
            return False

        # Why check all opponent pieces? Any can potentially attack the king
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece and piece[1] != color:
                    if self.can_attack((x, y), king_pos):
                        return True
        return False

    # Why check attack capability? Determines if a piece can move to a position (ignoring turn)
    def can_attack(self, start, end):
        piece = self.board[start[1]][start[0]]
        if not piece:
            return False
        
        original_piece = self.board[end[1]][end[0]]
        self.board[end[1]][end[0]] = None  # Why temporarily remove? Simulates attack move
        
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        piece_type = piece[0]

        if piece_type == 'pawn':
            direction = -1 if piece[1] == 'white' else 1
            result = (abs(dx) == 1 and dy == direction)
        elif piece_type == 'rook':
            result = (dx == 0 or dy == 0) and self.is_path_clear(start, end)
        elif piece_type == 'knight':
            result = (abs(dx) == 2 and abs(dy) == 1) or (abs(dx) == 1 and abs(dy) == 2)
        elif piece_type == 'bishop':
            result = abs(dx) == abs(dy) and self.is_path_clear(start, end)
        elif piece_type == 'queen':
            result = ((dx == 0 or dy == 0) or (abs(dx) == abs(dy))) and self.is_path_clear(start, end)
        elif piece_type == 'king':
            result = abs(dx) <= 1 and abs(dy) <= 1
        else:
            result = False

        self.board[end[1]][end[0]] = original_piece  # Why restore? Maintains board state
        return result

    # Why check checkmate? Determines game end condition
    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False
        
        # Why check all possible moves? If no move gets king out of check, it is checkmate
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece and piece[1] == color:
                    for end_y in range(8):
                        for end_x in range(8):
                            if self.is_valid_move((x, y), (end_x, end_y)):
                                original_start = self.board[y][x]
                                original_end = self.board[end_y][end_x]
                                self.board[y][x] = None
                                self.board[end_y][end_x] = original_start
                                
                                if not self.is_in_check(color):
                                    self.board[y][x] = original_start
                                    self.board[end_y][end_x] = original_end
                                    return False
                                
                                self.board[y][x] = original_start
                                self.board[end_y][end_x] = original_end
        return True

    # Why move piece? Updates board state after validated move
    def move_piece(self, start, end):
        piece = self.board[start[1]][start[0]]
        self.board[start[1]][start[0]] = None
        self.board[end[1]][end[0]] = piece
        
        # Why switch player? Turn-based gameplay
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        
        # Why check for checkmate? Game ends when checkmate occurs
        if self.is_checkmate(self.current_player):
            self.game_over = True
            self.checkmate = True
            print(f'Checkmate! {self.current_player} wins!')
        elif self.is_in_check(self.current_player):
            print(f'Check! {self.current_player} is in check.')

    # Why parse input? Converts user input to board coordinates
    def parse_move(self, move_str):
        if len(move_str) != 4:
            return None
        start = (ord(move_str[0]) - ord('a'), 8 - int(move_str[1]))
        end = (ord(move_str[2]) - ord('a'), 8 - int(move_str[3]))
        return (start, end)

    # Why play loop? Main game interaction cycle
    def play(self):
        print('Simple Chess Game')
        print('Enter moves in format: e2e4 (from e2 to e4)')
        print('Type "quit" to exit')
        
        while not self.game_over:
            self.print_board()
            print(f"{self.current_player}'s turn")
            
            move_str = input('Enter your move: ').strip().lower()
            if move_str == 'quit':
                break
            
            move = self.parse_move(move_str)
            if not move:
                print('Invalid move format. Use format like: e2e4')
                continue
            
            start, end = move
            if self.is_valid_move(start, end):
                self.move_piece(start, end)
            else:
                print('Invalid move. Try again.')

if __name__ == '__main__':
    game = Chess()
    game.play()
