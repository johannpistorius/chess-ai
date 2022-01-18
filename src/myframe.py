import tkinter as tk


class MyFrame(tk.Frame):

    def __init__(self, parent, board, rows=8, columns=8, size=60, color1="#F5CBA7", color2="#AF601A"):
        self.parent = parent
        self.board = board
        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2

        self.turn = board.turn
        self.turn_data = board
        self.turn_data.bind_to(self.turn_manager)
        self.turn_data.bind_to(self.refresh)

        self.piece_hold = None

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, self.parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height)
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        self.canvas.bind("<Configure>", self.configure)
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<B1-Motion>", self.hold)
        self.canvas.bind("<ButtonRelease-1>", self.release)

        self.init_board()

    def init_board(self):
        for piece in self.board.pieces:
            self.place_piece(piece)

    def turn_manager(self, turn):
        self.turn = turn

    def place_piece(self, piece):
        column = self.board.convert_file_to_col(piece.square.file)
        row = self.board.convert_rank_to_row(piece.square.rank)
        x = (column * self.size) + int(self.size / 2)
        y = (row * self.size) + int(self.size / 2)
        if piece.color:
            self.canvas.create_text(x, y, fill="white", font="Times 20", text=piece.get_unicode(),
                                    tags="piece " + piece.square.file + piece.square.rank)
        else:
            self.canvas.create_text(x, y, fill="black", font="Times 20", text=piece.get_unicode(),
                                    tags="piece " + piece.square.file + piece.square.rank)

    def refresh(self, turn):
        #print("refresh")
        self.canvas.delete("select")
        self.canvas.delete("hold")
        self.canvas.delete("piece")
        self.init_board()

    def configure(self, event):
        xsize = int((event.width - 1) / self.columns)
        ysize = int((event.height - 1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        self.canvas.delete("piece")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        for piece in self.board.pieces:
            self.place_piece(piece)
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

    def click(self, event):
        self.canvas.delete("select")
        col = int(event.x / self.size)
        row = int(event.y / self.size)
        file = self.board.convert_col_to_file(col)
        rank = self.board.convert_row_to_rank(row)
        square = self.board.find_square(file, rank)
        if square is not None and square.piece is not None and square.piece.color is self.turn and \
                (self.board.player.color is self.turn and self.board.player.ishuman or
                 self.board.opponent.color is self.turn and self.board.opponent.ishuman):
            self.piece_hold = self.board.get_piece_on_square(rank, file)
            x1 = (int(col) * self.size)
            y1 = (int(row) * self.size)
            x2 = x1 + self.size
            y2 = y1 + self.size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="yellow", fill="", tags="select")
            for key, values in self.board.current_available_moves.items():
                if key is square.piece:
                    for value in values:
                        col = self.board.convert_file_to_col(value[0])
                        row = self.board.convert_rank_to_row(value[1])
                        x1 = (int(col) * self.size)
                        y1 = (int(row) * self.size)
                        x2 = x1 + self.size
                        y2 = y1 + self.size
                        square = self.board.find_square(value[0], value[1])
                        if square.piece is None:
                            self.canvas.create_rectangle(x1, y1, x2, y2, outline="yellow", fill="green", tags="select")
                        else:
                            self.canvas.create_rectangle(x1, y1, x2, y2, outline="yellow", fill="red", tags="select")

    def hold(self, event):
        self.canvas.delete("hold")
        if self.piece_hold is not None:
            if self.piece_hold.color:
                self.canvas.create_text(
                    event.x,
                    event.y,
                    fill="white",
                    font="Times 20",
                    text=self.piece_hold.get_unicode(),
                    tags="hold"
                )
            else:
                self.canvas.create_text(
                    event.x,
                    event.y,
                    fill="black",
                    font="Times 20",
                    text=self.piece_hold.get_unicode(),
                    tags="hold"
                )

    def release(self, event):
        self.canvas.delete("hold")
        col = int(event.x / self.size)
        row = int(event.y / self.size)
        file = self.board.convert_col_to_file(col)
        rank = self.board.convert_row_to_rank(row)
        square = self.board.find_square(file, rank)
        if self.piece_hold is not None:
            for key, values in self.board.current_available_moves.items():
                if key is self.piece_hold:
                    for value in values:
                        if value[0] == file and value[1] == rank:
                            self.board.place_piece(self.piece_hold, square)
                            self.canvas.delete("select")
                            self.board.turn = not self.board.turn
        self.piece_hold = None
