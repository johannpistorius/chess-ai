from piece import Piece


class Bishop(Piece):
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
        return available_moves

    def get_unicode(self):
        if self.color:
            return "\u2657"
        else:
            return "\u265d"

    def standard_algebraic_notation(self):
        if self.color:
            self.san = "B"
        else:
            self.san = "b"

    def get_points(self):
        return 3
