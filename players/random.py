import numpy as np
from othello import Env, Action

from .base import BasePlayer


class RandomPlayer(BasePlayer):
    def __init__(self):
        super(RandomPlayer, self).__init__()

    def reset(self) -> None:
        pass

    def play(self, env: Env) -> Action:
        actions = env.legal_actions()
        action = np.random.choice(actions)
        return action
