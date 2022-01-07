from piece import Piece


class Rook(Piece):
    def __init__(self, color, square=None, not_moved=True):
        super().__init__(color, square)
        self.standard_algebraic_notation()
        self.not_moved = not_moved

    #TODO add castling ability
    def available_moves(self, squares):
        available_moves = []
        rank = self.square.rank
        file = self.square.file
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
            return "\u2656"
        else:
            return "\u265c"

    def standard_algebraic_notation(self):
        if self.color:
            self.san = "R"
        else:
            self.san = "r"

    def get_points(self):
        return 5