import numpy as np
from othello import Action
from players.base import BasePlayer


class MyPlayer(BasePlayer):
    def __init__(self):
        super(MyPlayer, self).__init__()

    def reset(self) -> None:
        pass

    def play(self, env) -> Action:
        actions = env.legal_actions()
        action = np.random.choice(actions)
        return action
