import os
import sys
import argparse

import numpy as np
from othello import Env, Action

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


def score_fn(env: Env) -> int:
    if env.player.is_black():
        return np.sum(env.board * scores)
    else:
        return -np.sum(env.board * scores)


def minimax(env, move, depth) -> int:
    if env.is_done() or depth == 0:
        return -score_fn(env)

    actions = env.legal_actions()
    best_score = 0
    for action in actions:
        env.update(action)
        score = minimax(env, action, depth - 1)
        env.undo()

        best_score = max(best_score, score)

    return -best_score


class MinimaxPlayer(BasePlayer):
    MAX_DEPTH = 2

    def __init__(self):
        super(MinimaxPlayer, self).__init__()

    def reset(self) -> None:
        pass

    def play(self, env: Env) -> Action:
        actions = env.legal_actions()
        scores = np.zeros(len(actions), dtype="float64")
        for i, action in enumerate(actions):
            env.update(action)
            scores[i] = minimax(env, action, self.MAX_DEPTH)
            env.undo()

        return actions[np.argmax(scores)]
