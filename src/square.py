class Square:
    def __init__(self, rank, file, piece=None):
        self.rank = rank
        self.file = file
        self.piece = piece

    def __str__(self):
        return self.file+""+self.rank
