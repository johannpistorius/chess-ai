class Piece:
    def __init__(self, color, square=None):
        #self.san = ""
        self.color = color
        self.square = square
        if square is not None:
            self.set_position(square)

    def set_position(self, square):
        self.square.piece = None
        self.square = square
        self.square.piece = self

    def find_square(self, rank, file, squares):
        for square in squares:
           if square.rank == rank and square.file == file:
               return square
        return None

    def check_line(self, rank, file, rank_direction, file_direction, squares):
        available_moves = []
        square = self.find_square(str(int(rank) + rank_direction), chr(ord(file) + file_direction), squares)
        while square is not None and (square.piece is None or square.piece.color is not self.color):
            available_moves.append(str(square))
            if square.piece is not None and square.piece.color is not self.color:
                break
            rank = str(int(rank) + rank_direction)
            file = chr(ord(file) + file_direction)
            square = self.find_square(str(int(rank) + rank_direction), chr(ord(file) + file_direction), squares)
        return available_moves

    def __hash__(self):
        return hash((self.san, self.square.rank, self.square.file))

    def __eq__(self, other):
        return (self.san, self.square.rank, self.square.file) == (other.san, other.square.rank, other.square.file)

    def __str__(self):
        return self.san
