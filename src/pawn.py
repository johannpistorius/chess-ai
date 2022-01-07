from piece import Piece


class Pawn(Piece):
    def __init__(self, color, square=None):
        super().__init__(color, square)
        self.standard_algebraic_notation()

    def available_moves(self, squares):
        available_moves = []
        rank = self.square.rank
        file = self.square.file
        for i in self.check_forward(rank, file, squares):
            available_moves.append(i)
        for i in self.check_diagonal(rank, file, squares):
            available_moves.append(i)
        return available_moves

    # TODO separate into different functions
    # TODO add en passant move
    def check_forward(self, rank, file, squares):
        available_moves = []
        if self.color:
            square = self.find_square(str(int(rank) + 1), file, squares)
            if square is not None and not square.piece:
                available_moves.append(str(square))
                if int(rank) == 2:
                    square = self.find_square(str(int(rank) + 2), file, squares)
                    if square is not None and not square.piece:
                        available_moves.append(str(square))
        else:
            square = self.find_square(str(int(rank) - 1), file, squares)
            if square is not None and not square.piece:
                available_moves.append(str(square))
                if int(rank) == 7:
                    square = self.find_square(str(int(rank) - 2), file, squares)
                    if square is not None and not square.piece:
                        available_moves.append(str(square))
        return available_moves

    def check_diagonal(self, rank, file, squares):
        available_moves = []
        if self.color:
            square = self.find_square(str(int(rank) + 1), chr(ord(file) + 1), squares)
            if square is not None and square.piece is not None and square.piece.color is not self.color:
                available_moves.append(str(square))
            square = self.find_square(str(int(rank) + 1), chr(ord(file) - 1), squares)
            if square is not None and square.piece is not None and square.piece.color is not self.color:
                available_moves.append(str(square))
        else:
            square = self.find_square(str(int(rank) - 1), chr(ord(file) + 1), squares)
            if square is not None and square.piece is not None and square.piece.color is not self.color:
                available_moves.append(str(square))
            square = self.find_square(str(int(rank) - 1), chr(ord(file) - 1), squares)
            if square is not None and square.piece is not None and square.piece.color is not self.color:
                available_moves.append(str(square))
        return available_moves

    def check_promotion(self):
        if (self.color and self.square.rank == "8") or (not self.color and self.square.rank == "1"):
            return True
        else:
            return False

    def en_passant(self):
        # when a pawn makes a two-step advance from its starting position an there is an opponent's pawn on a square
        # next ot the destination square on an adjacent file, then the opponent's pawn can capture it, moving to the
        # square the pawn passed over. This can only be done on the very next turn, otherwise the right to do so is
        # forfeited
        print("TODO")

    def get_unicode(self):
        if self.color:
            return "\u2659"
        else:
            return "\u265f"

    def standard_algebraic_notation(self):
        if self.color:
            self.san = "P"
        else:
            self.san = "p"

    def get_points(self):
        return 1
