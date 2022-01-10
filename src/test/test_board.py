import pytest

from board import Board
from player import Player
from pawn import Pawn

configuration = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
player = Player(True, "default_name", True)
opponent = Player(True, "default_name", False)
board = Board(configuration, player, opponent)


def count_piece_type(san):
    count = 0
    for i in board.pieces:
        if i.san == san:
            count += 1
    return count


'''
Test that fen_notation_to_board works as intended when setting default chess board
'''


def test_num_pieces():
    count = 0
    for i in board.pieces:
        count += 1
    assert count == 32


def test_num_pawns_white():
    assert count_piece_type('P') == 8


def test_num_pawns_black():
    assert count_piece_type('p') == 8


def test_num_rooks_white():
    assert count_piece_type('R') == 2


def test_num_rooks_black():
    assert count_piece_type('r') == 2


def test_num_knights_white():
    assert count_piece_type('N') == 2


def test_num_knights_black():
    assert count_piece_type('n') == 2


def test_num_bishops_white():
    assert count_piece_type('B') == 2


def test_num_bishops_black():
    assert count_piece_type('b') == 2


def test_num_queen_white():
    assert count_piece_type('Q') == 1


def test_num_queen_black():
    assert count_piece_type('q') == 1


def test_num_king_white():
    assert count_piece_type('K') == 1


def test_num_king_black():
    assert count_piece_type('k') == 1


'''
Test board_to_fen_notation
'''


def test_board_to_fen_notation():
    fen = board.board_to_fen_notation()
    assert fen == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


'''
Test finding pieces
'''


def test_find_piece():
    ret_value = board.find_piece(rank="1", file="a")
    assert ret_value is not None


def test_find_none_piece():
    ret_value = board.find_piece(rank="3", file="c")
    assert ret_value is None


'''
Test removing pieces
'''


def test_remove_piece():
    piece = board.find_piece(rank="1", file="a")
    board.remove_piece(piece)
    ret_value = board.find_piece(rank="1", file="a")
    assert ret_value is None
