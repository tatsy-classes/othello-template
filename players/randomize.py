import argparse
import os
import random
import sys

from othello import Env, Move

PARENT_DIR = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(PARENT_DIR)
from players.base import BasePlayer


class RandomPlayer(BasePlayer):
    def __init__(self):
        super(RandomPlayer, self).__init__()

    def reset(self) -> None:
        # Nothing to do
        pass

    def play(self, env: Env) -> Move:
        moves = env.legal_moves()
        move = random.choice(moves)
        return move


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Othello player")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    player = RandomPlayer()
    player.run(args.verbose)
