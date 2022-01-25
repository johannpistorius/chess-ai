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
        sys.setrecursionlimit(10000)
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
        # print(f"Initializing {(self.fullmove_number == 1)}")
        if self.fullmove_number == 1:
            self.current_available_moves = self.all_available_moves_player(player)
        else:
            self.current_available_moves = self.filter_available_moves(self.all_available_moves_player(player))
        # print(f"Moves {self.current_available_moves}")
        if self._turn:
            king = self.get_piece('K')
        else:
            king = self.get_piece('k')
        if self.halfmove_clock >= 50 or \
                (not self.current_available_moves and not self.is_piece_attacked(king.square)):
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
            move = player.choose_move(self.current_available_moves)
            for key, value in move.items():
                self.place_piece(key, self.find_square(value[0], value[1]))
            self.turn = not self._turn

    def place_piece(self, piece, new_square):
        # update halfmove and fullmove
        self.update_halfmove_clock(piece, new_square.piece)
        self.update_fullmove_number(piece.color)
        # en passant
        if str(new_square) == self.en_passant:
            print(self.en_passant)
            if self._turn:
                p = self.get_piece_on_square(str(int(self.en_passant[1]) - 1), self.en_passant[0])
            else:
                p = self.get_piece_on_square(str(int(self.en_passant[1]) + 1), self.en_passant[0])
            p.square.piece = None
            self.remove_piece(p)
        if piece.san.lower() == "p":
            if abs(int(piece.square.rank) - int(new_square.rank)) > 1:
                if piece.color:
                    self.en_passant = piece.square.file + "3"
                else:
                    self.en_passant = piece.square.file + "6"
            else:
                self.en_passant = ""
        else:
            self.en_passant = ""
        # update castling
        if piece.san.lower() == "r":
            if piece.not_moved:
                if self._turn:
                    king = self.get_piece('K')
                    if str(piece.square) == "h1":
                        king.castling_king_side = False
                    elif str(piece.square) == "a1":
                        king.castling_queen_side = False
                else:
                    king = self.get_piece('k')
                    if str(piece.square) == "h8":
                        king.castling_king_side = False
                    elif str(piece.square) == "a8":
                        king.castling_queen_side = False
        # set piece to new position
        if new_square.piece:
            self.remove_piece(new_square.piece)
        piece.set_position(new_square)
        # pawn promotion
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
        return None

    def get_piece(self, san, square=None):
        for piece in self.pieces:
            if square:
                if piece.san == san and piece.square.rank == square.rank and piece.square.file == square.file:
                    return piece
            else:
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
        for move in end_positions_opponent:
            for key, value in move.items():
                if value == str(square):
                    return True
        return False

    def all_available_moves_player(self, player):
        available_moves = []
        for piece in self.pieces:
            if piece.color == player.color:
                moves = piece.available_moves(self.squares)
                for i in moves:
                    available_moves.append({piece: i})
        return available_moves

    def filter_available_moves(self, available_moves):
        moves = []
        fen = self.board_to_fen_notation()
        if self._turn:
            king = self.get_piece('K')
        else:
            king = self.get_piece('k')
        for i in available_moves:
            for key, value in i.items():
                board_copy = Board(fen, self.player, self.opponent, persistent_obj=True)
                piece_copy = board_copy.get_piece(key.san, key.square)
                board_copy.place_piece(piece_copy, board_copy.find_square(value[0], value[1]))
                king_copy = board_copy.get_piece(king.san)
                if not board_copy.is_piece_attacked(king_copy.square):
                    moves.append({key: value})
                del board_copy

        # Castling
        if self._turn:
            rook_queen_side = self.get_piece_on_square('1', 'a')
            rook_king_side = self.get_piece_on_square('1', 'h')
        else:
            rook_queen_side = self.get_piece_on_square('8', 'a')
            rook_king_side = self.get_piece_on_square('8', 'h')
        if king.not_moved and (not self.is_piece_attacked(king.square)) \
                and str(rook_king_side).lower() == 'r' and str(rook_queen_side).lower() == 'r':
            if rook_king_side.not_moved and king.castling_king_side:
                if self._turn:
                    if not (self.get_piece_on_square('1', 'f') or self.get_piece_on_square('1', 'g')) \
                            and not (self.is_piece_attacked('f1') or self.is_piece_attacked('g1')):
                        moves.append({king: 'g1', rook_king_side: 'f1'})
                else:
                    if not (self.get_piece_on_square('8', 'f') or self.get_piece_on_square('8', 'g')) \
                            and not(self.is_piece_attacked('f8') or self.is_piece_attacked('g8')):
                        moves.append({king: 'g8', rook_king_side: 'f8'})
            if rook_queen_side.not_moved and king.castling_queen_side:
                if self._turn:
                    if not (self.get_piece_on_square('1', 'b') or self.get_piece_on_square('1', 'c') \
                            or self.get_piece_on_square('1', 'd')) and not (self.is_piece_attacked('c1') \
                            or self.is_piece_attacked('d1')):
                        moves.append({king: 'c1', rook_queen_side: 'd1'})
                else:
                    if not (self.get_piece_on_square('8', 'b') or self.get_piece_on_square('8', 'c') \
                            or self.get_piece_on_square('8', 'd')) and not (self.is_piece_attacked('c8') \
                            or self.is_piece_attacked('d8')):
                        moves.append({king: 'c8', rook_queen_side: 'd8'})

        # en passant
        if self.en_passant:
            file = self.en_passant[0]
            if self._turn:
                square_left = self.find_square(chr(ord(file) - 1), '5')
                if square_left is not None and square_left.piece is not None and square_left.piece.san == 'P':
                    moves.append({square_left.piece: self.en_passant})
                square_right = self.find_square(chr(ord(file) + 1), '5')
                if square_right is not None and square_right.piece is not None and square_right.piece.san == 'P':
                    moves.append({square_right.piece: self.en_passant})
            else:
                square_left = self.find_square(chr(ord(file) - 1), '4')
                if square_left is not None and square_left.piece is not None and square_left.piece.san == 'p':
                    moves.append({square_left.piece: self.en_passant})
                square_right = self.find_square(chr(ord(file) + 1), '4')
                if square_right is not None and square_right.piece is not None and square_right.piece.san == 'p':
                    moves.append({square_right.piece: self.en_passant})
        # print(f"{str(moves)}")
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
        # This is the number of halfmoves since the last capture or pawn advance. The reason for this field is that
        # the value is used in the fifty-move rule.
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
        for piece in self.pieces:
            if piece.san == 'K':
                castling_king_side_white = piece.castling_king_side
                castling_queen_side_white = piece.castling_queen_side
            elif piece.san == 'k':
                castling_king_side_black = piece.castling_king_side
                castling_queen_side_black = piece.castling_queen_side
        if not (castling_king_side_white and castling_queen_side_white \
                and castling_king_side_black and castling_queen_side_black):
            fen_notation += " -"
        else:
            if castling_king_side_white:
                fen_notation += " K"
            if castling_queen_side_white:
                fen_notation += "Q"
            if castling_king_side_black:
                fen_notation += "k"
            if castling_queen_side_black:
                fen_notation += "q"
        # en passant target square
        if self.en_passant:
            fen_notation += " " + self.en_passant
        else:
            fen_notation += " -"
        # Halfmove clock
        fen_notation += " " + str(self.halfmove_clock)
        # Fullmove number
        fen_notation += " " + str(self.fullmove_number)
        # print(fen_notation)
        return fen_notation

    def fen_notation_to_board(self, fen_notation):
        # TODO en passant
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

            if color:
                check_king_side = 'K'
                check_queen_side = 'Q'
            else:
                check_king_side = 'k'
                check_queen_side = 'q'

            if c == Pawn(color).san:
                self.pieces.append(Pawn(color, self.find_square(file, rank)))
            elif c == Rook(color).san:
                if file == 'a':
                    not_moved = self.castling_availability(check_queen_side, fen_split[2])
                else:
                    not_moved = self.castling_availability(check_king_side, fen_split[2])
                self.pieces.append(Rook(color, self.find_square(file, rank), not_moved))
            elif c == Knight(color).san:
                self.pieces.append(Knight(color, self.find_square(file, rank)))
            elif c == Bishop(color).san:
                self.pieces.append(Bishop(color, self.find_square(file, rank)))
            elif c == Queen(color).san:
                self.pieces.append(Queen(color, self.find_square(file, rank)))
            elif c == King(color).san:
                castling_king_side = self.castling_availability(check_king_side, fen_split[2])
                castling_queen_side = self.castling_availability(check_queen_side, fen_split[2])
                not_moved = (castling_king_side and castling_queen_side)
                self.pieces.append(
                    King(color, self.find_square(file, rank), not_moved, castling_king_side, castling_queen_side))
            file = chr(ord(file) + 1)
        self.halfmove_clock = int(fen_split[4])
        self.fullmove_number = int(fen_split[5])
        if fen_split[1] == "w":
            self.turn = True
        else:
            self.turn = False

    def castling_availability(self, val, fen_castling):
        if val in fen_castling:
            return True
        else:
            return False

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
