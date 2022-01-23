import random


class Player:
    def __init__(self, ishuman, name="default_name", color=None):
        self.ishuman = ishuman
        self.name = name
        self.color = color

    def choose_move(self, available_moves):
        return random.choice(available_moves)
