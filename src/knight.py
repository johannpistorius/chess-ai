from piece import Piece


class Knight(Piece):
    def __init__(self, color, square=None):
        super().__init__(color, square)
        self.standard_algebraic_notation()

    def available_moves(self, squares):
        available_moves = []
        rank = self.square.rank
        file = self.square.file
        for i in self.check_L_shape(rank, file, squares):
            available_moves.append(i)
        return available_moves

    def check_L_shape(self, rank, file, squares):
        available_moves = []
        square = self.find_square(str(int(rank) + 1), chr(ord(file) + 2), squares)
        if square is not None and (square.piece is None or square.piece.color is not self.color):
            available_moves.append(str(square))
        square = self.find_square(str(int(rank) + 2), chr(ord(file) + 1), squares)
        if square is not None and (square.piece is None or square.piece.color is not self.color):
            available_moves.append(str(square))
        square = self.find_square(str(int(rank) + 2), chr(ord(file) - 1), squares)
        if square is not None and (square.piece is None or square.piece.color is not self.color):
            available_moves.append(str(square))
        square = self.find_square(str(int(rank) + 1), chr(ord(file) - 2), squares)
        if square is not None and (square.piece is None or square.piece.color is not self.color):
            available_moves.append(str(square))
        square = self.find_square(str(int(rank) - 1), chr(ord(file) - 2), squares)
        if square is not None and (square.piece is None or square.piece.color is not self.color):
            available_moves.append(str(square))
        square = self.find_square(str(int(rank) - 2), chr(ord(file) - 1), squares)
        if square is not None and (square.piece is None or square.piece.color is not self.color):
            available_moves.append(str(square))
        square = self.find_square(str(int(rank) - 2), chr(ord(file) + 1), squares)
        if square is not None and (square.piece is None or square.piece.color is not self.color):
            available_moves.append(str(square))
        square = self.find_square(str(int(rank) - 1), chr(ord(file) + 2), squares)
        if square is not None and (square.piece is None or square.piece.color is not self.color):
            available_moves.append(str(square))
        return available_moves

    def get_unicode(self):
        if self.color:
            return "\u2658"
        else:
            return "\u265e"

    def standard_algebraic_notation(self):
        if self.color:
            self.san = "N"
        else:
            self.san = "n"

    def get_points(self):
        return 3
