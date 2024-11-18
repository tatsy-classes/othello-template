import os
import sys
import random
import argparse

from othello import Env, Action

PARENT_DIR = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(PARENT_DIR)
from players.base import BasePlayer


class RandomPlayer(BasePlayer):
    def __init__(self):
        super(RandomPlayer, self).__init__()

    def reset(self) -> None:
        pass

    def play(self, env: Env) -> Action:
        actions = env.legal_actions()
        action = random.choice(actions)
        return action
