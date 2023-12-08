import argparse
import random

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Othello player")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    player = MyPlayer()
    player.run(args.verbose)
