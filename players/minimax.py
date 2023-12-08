import argparse
import os
import sys

import numpy as np
from othello import Env, Move

PARENT_DIR = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(PARENT_DIR)
from players.base import BasePlayer

scores = np.array(
    [
        [120, -20, 20, 5, 5, 20, -20, 120],
        [-20, -40, -5, -5, -5, -5, -40, -20],
        [20, -5, 15, 3, 3, 15, -5, 20],
        [5, -5, 3, 0, 0, 3, -5, 5],
        [5, -5, 3, 0, 0, 3, -5, 5],
        [20, -5, 15, 3, 3, 15, -5, 20],
        [-20, -40, -5, -5, -5, -5, -40, -20],
        [120, -20, 20, 5, 5, 20, -20, 120],
    ],
    dtype="int32",
)


def minimax(env, move, depth, max_depth):
    env.update(move)

    if depth >= max_depth:
        score = move.player * np.sum(env.board * scores)
    else:
        # Calculate best score for opponent
        best_score = -np.inf
        for next_move in env.legal_moves():
            score = minimax(env, next_move, depth + 1, max_depth)
            if best_score < score:
                best_score = score

        # The best for opponent means negative for the player
        score = -best_score

    env.undo()
    return score


class MinimaxPlayer(BasePlayer):
    MAX_DEPTH = 2

    def __init__(self):
        super(MinimaxPlayer, self).__init__()

    def reset(self) -> None:
        # Nothing to do
        pass

    def play(self, env: Env) -> Move:
        moves = env.legal_moves()
        best_move = moves[0]
        best_score = -np.inf
        for move in moves:
            score = minimax(env, move, 0, self.MAX_DEPTH)
            if best_score < score:
                best_move = move
                best_score = score

        return best_move


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Othello player")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    player = MinimaxPlayer()
    player.run(args.verbose)
