from pawn import Pawn
from queen import Queen
from king import King
from bishop import Bishop
from knight import Knight
from rook import Rook
from square import Square

import sys

class Board:

    def __init__(self, configuration, player, opponent, rows=8, columns=8, persistent_obj=None):
        sys.setrecursionlimit(1000000)
        self.player = player
        self.opponent = opponent
        self.rows = rows
        self.columns = columns
        self.squares = []
        self.pieces = []
        self.pieces_captured = []

        self._turn = None
        self.turn_observers = []

        self.en_passant = ""
        self.fullmove_number = 1
        self.halfmove_clock = 0

        self.persistent_obj = persistent_obj
        self.init_board(configuration)

    @property
    def turn(self):
        return self._turn

    @turn.setter
    def turn(self, val):
        self._turn = val
        if not self.persistent_obj:
            player = self.get_player(self._turn)
            self.play(player)
        for callback in self.turn_observers:
            callback(self._turn)

    def bind_to(self, callback):
        self.turn_observers.append(callback)

    def init_board(self, configuration):
        # Init squares of the board
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                self.squares.append(Square(str(8 - i), chr(97 + j)))
        # Get game state
        self.fen_notation_to_board(configuration)

    def play(self, player):
        # TODO Random AI (not very smort)
        #print(f"Initializing {(self.fullmove_number == 1)}")
        if self.fullmove_number == 1:
            self.current_available_moves = self.all_available_moves_player(player)
        else:
            self.current_available_moves = self.filter_available_moves(self.all_available_moves_player(player))
        print(f"Moves {self.current_available_moves}")
        if self.halfmove_clock >= 50:
            print(self.board_to_fen_notation())
            print(str(self))
            sys.exit("Draw!")
        if not self.current_available_moves:
            print(self.board_to_fen_notation())
            print(str(self))
            if self._turn:
                sys.exit("Black won!")
            else:
                sys.exit("White won!")
        if player.color is self._turn and not player.ishuman:
            piece, position = player.choose_move(self.current_available_moves)
            self.place_piece(piece, self.find_square(position[0], position[1]))
            self.turn = not self._turn

    def place_piece(self, piece, new_square):
        self.update_halfmove_clock(piece, new_square.piece)
        self.update_fullmove_number(piece.color)
        if new_square.piece:
            self.remove_piece(new_square.piece)
        piece.set_position(new_square)
        if piece.san.lower() == "p":
            if piece.check_promotion():
                self.promote_pawn(piece)

    def remove_piece(self, piece):
        self.pieces.remove(piece)
        self.pieces_captured.append(piece)

    def get_piece_on_square(self, rank, file):
        for piece in self.pieces:
            if piece.square.rank == rank and piece.square.file == file:
                return piece

    def get_piece(self, san):
        for piece in self.pieces:
            if piece.san == san:
                return piece

    def find_square(self, file, rank):
        for square in self.squares:
            if square.rank == rank and square.file == file:
                return square

    def get_player(self, turn):
        if self.player.color is turn:
            return self.player
        if self.opponent.color is turn:
            return self.opponent

    def is_piece_attacked(self, square):
        end_positions_opponent = self.all_available_moves_player(self.get_player(not self._turn))
        for key, values in end_positions_opponent.items():
            for value in values:
                if value == str(square):
                    return True
        return False

    def all_available_moves_player(self, player):
        available_moves = {}
        for piece in self.pieces:
            if piece.color == player.color:
                moves = piece.available_moves(self.squares)
                if moves:
                    available_moves[piece] = moves
        return available_moves

    def filter_available_moves(self, available_moves):
        # print(f"Before \n {str(available_moves)}")
        moves = {}
        fen = self.board_to_fen_notation()
        king = None
        for piece in self.pieces:
            if piece.san.lower() == "k" and piece.color is self._turn:
                king = piece
        for key, values in list(available_moves.items()):
            #print(f"Key: {str(key)}")
            #print(f"Values: {str(values)}")
            for value in values:
                #print(f"\tIterating over: {str(value)}")
                board_copy = Board(fen, self.player, self.opponent, persistent_obj=True)
                #print(f"\tBoard: {str(board_copy.board_to_fen_notation())}")
                piece_copy = board_copy.get_piece(key.san)
                board_copy.place_piece(piece_copy, board_copy.find_square(value[0], value[1]))
                king_copy = board_copy.get_piece(king.san)
                #print(f"\tKing: {str(king_copy.square)}")
                if not board_copy.is_piece_attacked(king_copy.square):
                    #print(f"\tKing not in check if: {str(key)} to {str(value)}")
                    if key in moves:
                        moves[key].append(value)
                    else:
                        moves[key] = [value]
                #else:
                    #print(f"\tKing still in check if: {str(key)} to {str(value)}")
                del board_copy
        #print(f"After \n {str(moves)}")
        return moves

    # Special conditions
    def promote_pawn(self, piece):
        self.pieces.remove(piece)
        self.pieces.append(Queen(piece.color, self.find_square(piece.square.file, piece.square.rank)))

    def en_passant(self):
        # TODO
        # check opponent made a double forward pawn last turn and check pawn is next to that pawn
        print("TODO")

    def castling(self):
        # TODO
        # test if squares passed over by the king are not attacked : is_attacked
        # test that pieces have not moved
        print("TODO")

    def update_halfmove_clock(self, piece, capture):
        # This is the number of halfmoves since the last capture or pawn advance. The reason for this field is that the value is used in the fifty-move rule.
        if piece.san.lower() == "p" or capture:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

    def update_fullmove_number(self, color):
        # The number of the full move. It starts at 1, and is incremented after Black's move.
        if not color:
            self.fullmove_number += 1

    def checkmate(self, player):
        self.current_available_moves = self.filter_available_moves(self.all_available_moves_player(player))
        return not bool(self.current_available_moves)

    def convert_file_to_col(self, file):
        if self.player.color:
            return ord(file) - 97
        else:
            return 104 - ord(file)

    def convert_rank_to_row(self, rank):
        if self.player.color:
            return 8 - int(rank)
        else:
            return int(rank) - 1

    def convert_col_to_file(self, col):
        if self.player.color:
            return chr(col + 97)
        else:
            return chr(104 - col)

    def convert_row_to_rank(self, row):
        if self.player.color:
            return str(8 - row)
        else:
            return str(row + 1)

    def board_to_fen_notation(self):
        # Starting position in FEN notation
        # from a -> h
        # from 8 -> 1
        fen_notation = ""
        rank = "8"
        counter = 0
        # piece placement from white's perspective
        for square in self.squares:
            if square.piece is not None:
                if counter != 0:
                    fen_notation += str(counter)
                    counter = 0
                if square.rank != rank:
                    fen_notation += "/"
                    rank = square.rank
                fen_notation += square.piece.san
            else:
                if square.rank != rank:
                    if counter != 0:
                        fen_notation += str(counter)
                    fen_notation += "/"
                    rank = square.rank
                    counter = 1
                else:
                    counter += 1
        if counter != 0:
            fen_notation += str(counter)
        # active color
        if self._turn:
            fen_notation += " w"
        else:
            fen_notation += " b"
        # castling availability
        # TODO
        fen_notation += " KQkq"
        # en passant target square
        # TODO
        fen_notation += " -"
        # Halfmove clock
        fen_notation += " " + str(self.halfmove_clock)
        # Fullmove number
        fen_notation += " " + str(self.fullmove_number)
        # print(fen_notation)
        return fen_notation

    def fen_notation_to_board(self, fen_notation):
        # TODO castling/en passant
        # KQkq -
        color = True
        file = "a"
        rank = "8"
        fen_split = fen_notation.split()
        for c in fen_split[0]:
            if c == "/":
                file = "a"
                rank = str(int(rank) - 1)
                continue
            elif c.isnumeric():
                file = chr(ord(file) + int(c))
                continue
            elif c.islower():
                color = False
            elif c.isupper():
                color = True
            if c == Pawn(color).san:
                self.pieces.append(Pawn(color, self.find_square(file, rank)))
            elif c == Rook(color).san:
                self.pieces.append(Rook(color, self.find_square(file, rank)))
            elif c == Knight(color).san:
                self.pieces.append(Knight(color, self.find_square(file, rank)))
            elif c == Bishop(color).san:
                self.pieces.append(Bishop(color, self.find_square(file, rank)))
            elif c == Queen(color).san:
                self.pieces.append(Queen(color, self.find_square(file, rank)))
            elif c == King(color).san:
                self.pieces.append(King(color, self.find_square(file, rank)))
            file = chr(ord(file) + 1)
        self.halfmove_clock = int(fen_split[4])
        self.fullmove_number = int(fen_split[5])
        if fen_split[1] == "w":
            self.turn = True
        else:
            self.turn = False

    def __str__(self):
        board_text = ""
        fen = self.board_to_fen_notation()
        fens = fen.split()[0].split("/")
        for row in fens:
            for i in range(0, len(row)):
                if row[i].isdigit():
                    for j in range(0, int(row[i])):
                        board_text += ". "
                else:
                    board_text += row[i] + " "
            board_text += "\n"
        return board_text
