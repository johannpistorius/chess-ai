from piece import Piece


class King(Piece):
    def __init__(self, color, square=None, not_moved=True, castling_king_side=True, castling_queen_side=True):
        super().__init__(color, square)
        self.standard_algebraic_notation()
        self.not_moved = not_moved
        self.castling_king_side = castling_king_side
        self.castling_queen_side = castling_queen_side

    def set_position(self, square):
        self.square.piece = None
        self.square = square
        self.square.piece = self
        self.not_moved = False
        self.castling_king_side = False
        self.castling_queen_side = False

    def available_moves(self, squares):
        available_moves = []
        rank = self.square.rank
        file = self.square.file
        square = self.find_square(str(int(rank) + 1), chr(ord(file) + 1), squares)
        if square is not None and (square.piece is None or square.piece.color is not self.color):
            available_moves.append(str(square))
        square = self.find_square(str(int(rank) + 1), chr(ord(file)), squares)
        if square is not None and (square.piece is None or square.piece.color is not self.color):
            available_moves.append(str(square))
        square = self.find_square(str(int(rank) + 1), chr(ord(file) - 1), squares)
        if square is not None and (square.piece is None or square.piece.color is not self.color):
            available_moves.append(str(square))
        square = self.find_square(str(int(rank)), chr(ord(file) - 1), squares)
        if square is not None and (square.piece is None or square.piece.color is not self.color):
            available_moves.append(str(square))
        square = self.find_square(str(int(rank) - 1), chr(ord(file) - 1), squares)
        if square is not None and (square.piece is None or square.piece.color is not self.color):
            available_moves.append(str(square))
        square = self.find_square(str(int(rank) - 1), chr(ord(file)), squares)
        if square is not None and (square.piece is None or square.piece.color is not self.color):
            available_moves.append(str(square))
        square = self.find_square(str(int(rank) - 1), chr(ord(file) + 1), squares)
        if square is not None and (square.piece is None or square.piece.color is not self.color):
            available_moves.append(str(square))
        square = self.find_square(str(int(rank)), chr(ord(file) + 1), squares)
        if square is not None and (square.piece is None or square.piece.color is not self.color):
            available_moves.append(str(square))
        return available_moves

    def get_unicode(self):
        if self.color:
            return "\u2654"
        else:
            return "\u265a"

    def standard_algebraic_notation(self):
        if self.color:
            self.san = "K"
        else:
            self.san = "k"

    def get_points(self):
        return 4
