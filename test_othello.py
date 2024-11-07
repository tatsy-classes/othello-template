import sys

import numpy as np
import pytest
import othello
from player import MyPlayer
from othello import Player
from players import RandomPlayer, MinimaxPlayer


@pytest.fixture(scope="session")
def n_match(pytestconfig):
    return pytestconfig.getoption("n_match")


def game(p1_, p2_, n_match: int):
    n_win1 = 0
    n_win2 = 0
    print("")
    for i in range(n_match):
        env = othello.make()
        env.reset()

        if np.random.random() < 0.5:
            p1 = p1_
            p2 = p2_
        else:
            p1 = p2_
            p2 = p1_

        while not env.is_done():
            if env.player == Player.BLACK:
                action = p1.play(env)
            else:
                action = p2.play(env)

            env.update(action)

        n_black = env.count(Player.BLACK)
        n_white = env.count(Player.WHITE)
        if n_black > n_white:
            n_win1 += 1 if p1 is p1_ else 0
            n_win2 += 1 if p1 is p2_ else 0
            if p1 is p1_:
                print("x", end="")
            else:
                print("o", end="")
        elif n_black < n_white:
            n_win1 += 1 if p1 is p2_ else 0
            n_win2 += 1 if p1 is p1_ else 0
            if p1 is p1_:
                print("o", end="")
            else:
                print("x", end="")

        else:
            print("-", end="")

        if (i + 1) % 20 == 0:
            print("")
            print(f"{n_win2}/{n_match:d} ({100.0 * n_win2 / n_match:.1f}%)")

        sys.stdout.flush()

    return n_win1, n_win2


def test_randomize(n_match: int) -> None:
    p1 = RandomPlayer()
    p2 = MyPlayer()
    n1, n2 = game(p1, p2, n_match)
    ratio = n2 / n_match
    assert ratio > 0.7, f"win ratio is not too high: {100.0 * ratio:.1f}%"


def test_minimax(n_match: int) -> None:
    p1 = MinimaxPlayer()
    p2 = MyPlayer()
    n1, n2 = game(p1, p2, n_match)
    ratio = n2 / n_match
    assert ratio > 0.7, f"win ratio is not too high: {100.0 * ratio:.1f}%"
