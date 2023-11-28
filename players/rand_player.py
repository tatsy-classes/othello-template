import os
import sys
import random

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from othello import Env, Move
from players.base import BasePlayer


class RandomPlayer(BasePlayer):
    def __init__(self):
        super(RandomPlayer, self).__init__()

    def reset(self) -> None:
        # Nothing to do
        pass

    def play(self, env: Env) -> Move:
        moves = env.legal_moves()
        if len(moves) != 0:
            move = random.choice(moves)
        else:
            move = Move.Pass(env.player)

        return move


if __name__ == "__main__":
    player = RandomPlayer()
    player.run()
