class Moves:
    def __init__(self, squares, pieces, color):
        self.available_moves = {}
        self.squares = squares
        self.pieces = pieces
        self.color = color

    def get_available_moves(self):
        for piece in self.pieces:
            if piece.color == self.color:


    def pawn(self, rank, file, color):

    def bishop(self, rank, file):

    def knight(self, rank, file):

    def rook(self, rank, file):

    def queen(self, rank, file):

    def king(self, rank, file):

    def check_square_not_empty(self, rank, file):
