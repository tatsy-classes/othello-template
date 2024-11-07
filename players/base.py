from abc import ABC, abstractmethod

import colorama
from othello import Env, Move


class BasePlayer(ABC):
    def __init__(self):
        colorama.init(strip=False)
        self.verbose = False
        self.name = self.__class__.__name__
        self.reset()

    def reset(self) -> None:
        pass

    @abstractmethod
    def play(self, env: Env) -> Move:
        pass
