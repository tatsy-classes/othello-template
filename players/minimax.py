import time

import numpy as np
from othello import Env, Action, Player

from .base import BasePlayer

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
    dtype="float64",
)


def score_fn(env: Env, current_player: Player) -> int:
    if current_player.is_black():
        return np.sum(env.board * scores)
    elif current_player.is_white():
        return -np.sum(env.board * scores)
    else:
        raise ValueError("Invalid player")


def minimax(env, current_player, depth) -> float:
    if env.is_done() or depth == 0:
        return score_fn(env, current_player)

    actions = env.legal_actions()
    if env.player == current_player:
        best_score = -np.inf
        for action in actions:
            env.update(action)
            score = minimax(env, current_player, depth - 1)
            env.undo()
            best_score = max(best_score, score)
    else:
        best_score = np.inf
        for action in actions:
            env.update(action)
            score = minimax(env, current_player, depth - 1)
            env.undo()
            best_score = min(best_score, score)

    return best_score


class MinimaxPlayer(BasePlayer):
    TIME_LIMIT = 1.0e-2

    def __init__(self):
        super(MinimaxPlayer, self).__init__()

    def reset(self) -> None:
        pass

    def play(self, env: Env) -> Action:
        current_player = env.player
        actions = env.legal_actions()

        best_action = actions[0]
        best_score = -np.inf
        max_depth = 0
        start_time = time.perf_counter()
        while time.perf_counter() - start_time < self.TIME_LIMIT:
            for i, action in enumerate(actions):
                env.update(action)
                v = minimax(env, current_player, max_depth)
                env.undo()

                if best_score < v:
                    best_score = v
                    best_action = action

            max_depth += 1

        return best_action
