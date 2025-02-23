import os
import multiprocessing
from board import Board
from player import Player

def build_board(config):
    """Creates a chess board instance with two players."""
    player = Player(ishuman=False, name="AI_1", color=True)  # AI player
    if not player.ishuman:
        player.load_model()
    opponent = Player(ishuman=False, name="AI_2", color=False)  # AI opponent
    if not opponent.ishuman:
        opponent.load_model();
    return Board(config, player, opponent, on_game_over=on_game_over)

def on_game_over(board, message):
    """Callback function when the game ends."""
    print(message)
    if not board.player.ishuman:
        board.player.save_model()
    if not board.opponent.ishuman:
        board.opponent.save_model()

def play_headless_game(config, game_id):
    """Runs a game without GUI."""
    build_board(config)


def run_gui_game(config):
    """Runs a game with a Tkinter GUI."""
    import tkinter as tk
    from myframe import MyFrame

    board = build_board(config)
    root = tk.Tk()
    root.title("Chess")
    
    parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    filename = os.path.join(parent, 'res', 'icon', 'icon.ico')
    root.iconbitmap(filename)

    my_frame = MyFrame(root, board)
    my_frame.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    root.mainloop()

if __name__ == "__main__":
    configuration = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    
    mode = input("Enter mode (gui/headless): ").strip().lower()

    if mode == "gui":
        run_gui_game(configuration)
    elif mode == "headless":
        num_games = 5  # Number of parallel headless games
        processes = []
        for i in range(num_games):
            p = multiprocessing.Process(target=play_headless_game, args=(configuration, i))
            p.start()
            processes.append(p)
        
        for p in processes:
            p.join()
    else:
        print("Invalid mode. Choose 'gui' or 'headless'.")
