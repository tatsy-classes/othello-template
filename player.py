import sys
import pickle
import random
import socket
import argparse
import subprocess

import numpy as np
import colorama
from server import MatchServer
from othello import Env, Move
from colorama import Fore


class BasePlayer(object):
    def __init__(self):
        colorama.init()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((MatchServer.TCP_IP, MatchServer.TCP_PORT))
        self.bufsize = MatchServer.BUF_SIZE

    def print(self, msg, *args, **kwargs):
        print(Fore.GREEN + "[CLIENT]: " + Fore.RESET, end="")
        print(msg, *args, **kwargs)
        sys.stdout.flush()

    def play(self, env: Env) -> Move:
        raise NotImplementedError()

    def run(self):
        self.sock.send(bytes("ready", "ascii"))
        while True:
            msg = self.sock.recv(self.bufsize).decode("ascii")
            if msg == "finish":
                break

            if msg != "go":
                raise Exception("Match server might submit 'go' before match starts!!")

            data = self.sock.recv(self.bufsize)
            env = pickle.loads(data)

            move = self.play(env)
            print(move)
            self.sock.send(pickle.dumps(move))


class RandomPlayer(BasePlayer):
    def __init__(self):
        super(RandomPlayer, self).__init__()

    def play(self, env: Env) -> Move:
        moves = env.legal_moves()
        if len(moves) != 0:
            move = random.choice(moves)
        else:
            move = Move.Pass(env.player)

        return move


def get_player(name: str) -> BasePlayer:
    if name == "random":
        return RandomPlayer()
    else:
        raise Exception(f"Player with name {name:s} is not registered!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch othello player")
    parser.add_argument("--name", type=str, default="random", choices=["random"])
    args = parser.parse_args()

    player = get_player(args.name)
    player.run()
