from piece import Piece


class Queen(Piece):
    def __init__(self, color, square=None):
        super().__init__(color, square)
        self.standard_algebraic_notation()

    def available_moves(self, squares):
        available_moves = []
        rank = self.square.rank
        file = self.square.file
        for i in self.check_line(rank, file, 1, 1, squares):
            available_moves.append(i)
        for i in self.check_line(rank, file, 1, -1, squares):
            available_moves.append(i)
        for i in self.check_line(rank, file, -1, -1, squares):
            available_moves.append(i)
        for i in self.check_line(rank, file, -1, 1, squares):
            available_moves.append(i)
        for i in self.check_line(rank, file, 1, 0, squares):
            available_moves.append(i)
        for i in self.check_line(rank, file, 0, -1, squares):
            available_moves.append(i)
        for i in self.check_line(rank, file, -1, 0, squares):
            available_moves.append(i)
        for i in self.check_line(rank, file, 0, 1, squares):
            available_moves.append(i)
        return available_moves

    def get_unicode(self):
        if self.color:
            return "\u2655"
        else:
            return "\u265b"

    def standard_algebraic_notation(self):
        if self.color:
            self.san = "Q"
        else:
            self.san = "q"

    def get_points(self):
        return 9
