import random
import argparse

from othello import Move
from players.base import BasePlayer


class MyPlayer(BasePlayer):
    def __init__(self):
        super(MyPlayer, self).__init__()

    def reset(self) -> None:
        pass

    def play(self, env) -> Move:
        moves = env.legal_moves()
        move = random.choice(moves)
        return move
