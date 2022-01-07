from piece import Piece


class King(Piece):
    def __init__(self, color, square=None, not_moved=True):
        super().__init__(color, square)
        self.standard_algebraic_notation()
        self.not_moved = not_moved

    # TODO add castling ability
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

    def castling(self):
        # neither the king nor the rook has previously moved during the game
        # there are no pieces between the king and the rook
        # the king is not in check, and will not pass through or land on any square attacked by an enemy piece
        # (castling is permitted if the rook is under attack)
        print("TODO")

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
