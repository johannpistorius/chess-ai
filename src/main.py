import tkinter as tk
from login import Login
from myframe import MyFrame
from board import Board
from player import Player
import os
import threading


def build_board(config):
    player = Player(ishuman=False, name="default_name", color=True)
    opponent = Player(ishuman=False, name="default_name", color=False)
    board = Board(config, player, opponent)
    return board


def create_game(board):
    parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    filename = os.path.join(parent, 'res', 'icon', 'icon.ico')

    root = tk.Tk()
    root.title("Chess")
    root.iconbitmap(filename)

    # login = Login(root)
    # login.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    my_frame = MyFrame(root, board)
    my_frame.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    root.mainloop()


if __name__ == "__main__":
    configuration = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    # configuration = "6k1/5p2/6p1/8/7p/8/6PP/6K1 b - - 0 0"
    t1 = threading.Thread(target=create_game(build_board(configuration))).start()
