from abc import ABC, abstractmethod

import colorama
from othello import Env, Action


class BasePlayer(ABC):
    def __init__(self):
        colorama.init(strip=False)
        self.verbose = False
        self.name = self.__class__.__name__

    def reset(self) -> None:
        pass

    @abstractmethod
    def play(self, env: Env) -> Action:
        pass
