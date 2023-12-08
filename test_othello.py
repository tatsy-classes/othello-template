import os

import pytest

from match import match

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
MY_FILE = os.path.join(CUR_DIR, "player.py")


def check(path: str) -> None:
    if not os.path.exists(path):
        raise FileExistsError("File not found:" + path)

    b_win, w_win, _ = match(MY_FILE, path, 100, True)
    assert (b_win - w_win) >= 20, "Your othello AI is not quite strong..."


def test_solve(path: str):
    check(path)


@pytest.fixture(scope="session")
def path(pytestconfig):
    return pytestconfig.getoption("path")
