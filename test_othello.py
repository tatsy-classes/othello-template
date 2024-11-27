import sys
import argparse

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
        p1_.reset()
        p2_.reset()

        if np.random.random() < 0.5:
            p1 = p1_
            p2 = p2_
        else:
            p1 = p2_
            p2 = p1_

        while not env.is_done():
            actions = env.legal_actions()
            if len(actions) == 0:
                env.turn_change()
                continue

            if env.player.is_black():
                action = p1.play(env)
            elif env.player.is_white():
                action = p2.play(env)
            else:
                raise ValueError("Invalid player")

            env.update(action)

        n_black = env.count(Player.BLACK)
        n_white = env.count(Player.WHITE)
        if n_black > n_white:
            n_win1 += 1 if p1 is p1_ else 0
            n_win2 += 1 if p1 is p2_ else 0
            if p1 is p1_:
                print("o", end="")
            else:
                print("x", end="")
        elif n_black < n_white:
            n_win1 += 1 if p1 is p2_ else 0
            n_win2 += 1 if p1 is p1_ else 0
            if p1 is p1_:
                print("x", end="")
            else:
                print("o", end="")

        else:
            print("-", end="")

        if (i + 1) % 20 == 0:
            print("")
            print(f"{n_win1}/{i + 1:d} ({100.0 * n_win1 / (i + 1):.1f}%)")

        sys.stdout.flush()

    return n_win1, n_win2


def test_random(n_match: int):
    p1 = MyPlayer()
    p2 = RandomPlayer()
    n_win1, n_win2 = game(p1, p2, n_match)
    assert n_win1 > n_win2, "You lose to RandomPlayer"


def test_minimax(n_match: int):
    p1 = MyPlayer()
    p2 = MinimaxPlayer()
    n_win1, n_win2 = game(p1, p2, n_match)
    assert n_win1 > n_win2, "You lose to MinimaxPlayer"
